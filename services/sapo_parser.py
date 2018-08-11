import xml.etree.ElementTree as ET
from models.movie import Movie
from models.schedule import Schedule
from configs.config import CONFIG
import re

ns = {'sapo': CONFIG.NS}


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

        if _validate_movie(sapo_title):
            movie = Movie()
            movie.sapo_id = sapo_id
            movie.sapo_title = sapo_title
            movie.sapo_description = program.find('sapo:Description', ns).text
            movies.append(movie)

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
    return re.match(r'(.*) Ep\.\s\d+', sapo_title, flags=0) is None
