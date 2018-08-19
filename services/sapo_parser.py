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

    for program in root \
            .find('sapo:GetChannelByDateIntervalResult', ns) \
            .find('sapo:Programs', ns) \
            .findall('sapo:Program', ns):

        sapo_id = program.find('sapo:Id', ns).text
        sapo_title = program.find('sapo:Title', ns).text
        sapo_description = program.find('sapo:Description', ns).text

        if _validate_movie(sapo_title):

            mongo_result = ms.get_movie_in_db_by_name_and_description(sapo_title, sapo_description)

            # Only add new movie if does not exist
            if mongo_result is None:
                movie = Movie()
                movie.sapo_id = sapo_id
                movie.sapo_title = sapo_title
                movie.sapo_description = sapo_description
                movies.append(movie)

            else:
                movie = Movie(json.loads(dumps(mongo_result)))
                sapo_id = movie.sapo_id

            schedule = Schedule()
            schedule.sapo_id = sapo_id
            schedule.sapo_channel = root \
                .find('sapo:GetChannelByDateIntervalResult', ns) \
                .find('sapo:Sigla', ns).text
            schedule.sapo_start_datetime = program.find('sapo:StartTime', ns).text
            schedule.sapo_end_datetime = program.find('sapo:EndTime', ns).text
            schedule.sapo_end_datetime = program.find('sapo:Duration', ns).text
            schedules.append(schedule)

    return movies, schedules


# Validating whether it is valid movie
def _validate_movie(sapo_title):
    return _validate_movie_title_sapo(sapo_title)


# Validating if it is a series
def _validate_movie_title_sapo(sapo_title):
    return re.match(r'(.*) Ep\.\s\d+', sapo_title, flags=0) is None \
           and 'Grandes Realizadores' not in sapo_title \
           and 'Zoom In' not in sapo_title
