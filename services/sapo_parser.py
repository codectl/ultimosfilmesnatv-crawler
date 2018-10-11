# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
from bson.json_util import dumps
import json
import re
import services.movie_service as ms
from models.movie import Movie
from models.schedule import Schedule
from configs.config import CONFIG

ns = {'sapo': CONFIG.SAPO_NS}


def parse(response):
    root = ET.fromstring(response)

    movies = []
    schedules = []
    updates = []

    for program in root \
            .find('sapo:GetChannelByDateIntervalResult', ns) \
            .find('sapo:Programs', ns) \
            .findall('sapo:Program', ns):

        sapo_id = program.find('sapo:Id', ns).text
        sapo_title = program.find('sapo:Title', ns).text
        sapo_title = sapo_title.replace('(V.O.)', '').replace('(V.P.)', '').strip()
        sapo_description = program.find('sapo:Description', ns).text

        if _validate_movie(sapo_title):

            # Check if movie is saved under other movie entry
            movie = _resolve_movie(sapo_id, sapo_title, sapo_description)

            # Movie was successfully resolved
            if movie is not None:
                sapo_id = movie.sapo_id

                # Adding id alias
                if movie.sapo_id != sapo_id and sapo_id not in movie.alias_ids:
                    movie.alias_ids.append(sapo_id)
                    updates.append(movie)

                # Adding title alias
                if movie.sapo_title != sapo_title and sapo_title not in movie.alias_titles:
                    movie.alias_titles.append(sapo_title)
                    updates.append(movie)

            # Movie already in the list of movies to be added
            elif any(m.sapo_id == sapo_id for m in movies):
                pass

            # Getting alias_ids for movies not yet in persisted
            elif any(sapo_title.lower() == m.sapo_title.lower() for m in movies):
                movie = next(m for m in movies if sapo_title.lower() == m.sapo_title.lower())
                movie.alias_ids.append(sapo_id)

            # Otherwise add new one
            else:
                movie = Movie()
                movie.sapo_id = sapo_id
                movie.sapo_title = sapo_title
                movie.sapo_description = sapo_description
                movies.append(movie)

            schedule = Schedule()
            schedule.sapo_id = sapo_id
            schedule.sapo_channel = root \
                .find('sapo:GetChannelByDateIntervalResult', ns) \
                .find('sapo:Sigla', ns).text
            schedule.sapo_start_datetime = program.find('sapo:StartTime', ns).text
            schedule.sapo_end_datetime = program.find('sapo:EndTime', ns).text
            schedule.sapo_duration = program.find('sapo:Duration', ns).text
            schedules.append(schedule)

    return movies, schedules, updates


def _validate_movie(sapo_title):
    """Validating whether it is valid movie"""
    return _validate_movie_title_sapo(sapo_title)


def _validate_movie_title_sapo(sapo_title):
    """Validating if it is a series"""
    return re.match(r'(.*) Ep\.\s\d+', sapo_title, flags=0) is None \
           and 'Hollywood News'.lower() not in sapo_title.lower() \
           and 'Grandes Realizadores'.lower() not in sapo_title.lower() \
           and 'Zoom In'.lower() not in sapo_title.lower() \
           and 'Universo Syfy'.lower() not in sapo_title.lower() \
           and 'Fecho De Emissão'.lower() not in sapo_title.lower()


def _get_movie_from_list(movies, sapo_title, sapo_description):
    """Get movie from list of movies to add if exists"""
    for m in movies:
        if m.sapo_title == sapo_title and m.sapo_description == sapo_description:
            return m
    return None


def _resolve_movie(sapo_id, sapo_title, sapo_description):
    """Resolve movie based on id, title and description"""
    id_alias = Movie.from_pymongo(ms.get_movie_alias_by_id(sapo_id))  # Movie alias based on id
    if id_alias is None:
        same_titles = Movie.from_pymongo(ms.get_movie_in_db_by_title(sapo_title))  # Search by title
        title_aliases = Movie.from_pymongo(ms.get_movie_alias_by_title(sapo_title))  # Search by title aliases
        alias_candidates = same_titles + list(filter(lambda e: e.sapo_id not in [x.sapo_id for x in same_titles],
                                                     title_aliases))
        for alias_candidate in alias_candidates:
            if SequenceMatcher(None, alias_candidate.sapo_description, sapo_description).ratio() > 0.5:
                return alias_candidate  # Match found based on title

            for alias_of in ms.get_movie_aliasof_by_title(alias_candidate.sapo_title):
                if SequenceMatcher(None, alias_of['sapo_description'], sapo_description).ratio() > 0.5:
                    return Movie.from_pymongo(
                        ms.get_movie_in_db_by_id(alias_of['alias_of']))  # Match found based on alias

    else:
        return id_alias  # Match found based on id

    return None
