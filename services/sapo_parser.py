import xml.etree.ElementTree as ET
from models.movie import Movie
from configs.config import CONFIG
import re

ns = {'sapo': CONFIG.NS}


def parse(response):
    root = ET.fromstring(response.encode('utf-8'))

    for program in root \
            .find('sapo:GetChannelByDateIntervalResult', ns) \
            .find('sapo:Programs', ns) \
            .findall('sapo:Program', ns):

        id_sapo = program.find('sapo:Id', ns).text
        title_sapo = program.find('sapo:Title', ns).text

        if _validate_movie(title_sapo):
            movie = Movie()
            movie.id_sapo = id_sapo
            movie.title_sapo = title_sapo
            movie.description_sapo = program.find('sapo:Description', ns).text
            movie.duration = program.find('sapo:Duration', ns).text

            print movie

    return 1, 2

# Validating whether it is valid movie
def _validate_movie(title_sapo):
    return _validate_movie_title_sapo(title_sapo)


def _validate_movie_title_sapo(title_sapo):
    return re.match(r'(.*) Ep\.\s\d+', title_sapo, flags=0) is None
