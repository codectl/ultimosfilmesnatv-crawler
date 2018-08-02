import xml.etree.ElementTree as ET
from models.movie import Movie

ns = {'sapo': 'http://services.sapo.pt/Metadata/EPG'}

def parse(response):
    root = ET.fromstring(response.encode('utf-8'))

    for program in root\
        .find('sapo:GetChannelByDateIntervalResult', ns)\
        .find('sapo:Programs', ns)\
        .findall('sapo:Program', ns):

        movie = Movie()
        movie.id_sapo = program.find('sapo:Id', ns).text
        movie.title_pt = program.find('sapo:Title', ns).text
        movie.description_sapo = program.find('sapo:Description', ns).text
        movie.duration = program.find('sapo:Duration', ns).text

        print movie.id_sapo

    return 1, 2