# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
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
            movie_alias = ms.get_movie_alias(sapo_id)

            # Check if movie exists in db by name and description
            same_name_description_movie = ms.get_movie_in_db_by_name_and_description(sapo_title, sapo_description)

            # Movie has aliases
            if movie_alias is not None:
                movie = Movie(json.loads(dumps(movie_alias)))
                sapo_id = movie.sapo_id

            # Combine movie if already exists one of the same
            elif same_name_description_movie is not None:
                movie = Movie(json.loads(dumps(same_name_description_movie)))
                movie.aliases.append(sapo_id)
                updates.append(movie)
                sapo_id = movie.sapo_id

            # Movie already in the list of movies to be added
            elif any(m.sapo_id == sapo_id for m in movies):
                sapo_id = (next(m for m in movies if m.sapo_id == sapo_id)).sapo_id

            # Getting aliases for movies not yet in persisted
            elif any(sapo_title == m.sapo_title and sapo_description == m.sapo_description for m in movies):
                movie = next(m for m in movies if sapo_title == m.sapo_title and sapo_description == m.sapo_description)
                movie.aliases.append(sapo_id)

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
            schedule.duration = program.find('sapo:Duration', ns).text
            schedules.append(schedule)

    return movies, schedules, updates


# Validating whether it is valid movie
def _validate_movie(sapo_title):
    return _validate_movie_title_sapo(sapo_title)


# Validating if it is a series
def _validate_movie_title_sapo(sapo_title):
    return re.match(r'(.*) Ep\.\s\d+', sapo_title, flags=0) is None \
           and 'Hollywood News' not in sapo_title \
           and 'Grandes Realizadores' not in sapo_title \
           and 'Zoom In' not in sapo_title \
           and 'Universo Syfy' not in sapo_title \
           and 'Fecho De Emissão' not in sapo_title


# Get movie from list of movies to add if exists
def _get_movie_from_list(movies, sapo_title, sapo_description):
    for m in movies:
        if m.sapo_title == sapo_title and m.sapo_description == sapo_description:
            return m
    return None
