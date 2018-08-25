import configparser
from pymongo import MongoClient


class Properties:
    def __init__(self):
        pass


def load_properties():
    # Read configuration properties
    config = configparser.ConfigParser()
    config.read('configs/properties.ini')

    properties = Properties()
    properties.CHANNELS = config.get('general', 'channels')

    properties.DATABASE_ENDPOINT = config.get('database', 'endpoint')

    properties.SAPO_ENDPOINT = config.get('sapo', 'endpoint')
    properties.SAPO_IMAGE = config.get('sapo', 'image')
    properties.SAPO_NS = config.get('sapo', 'ns')

    properties.OMDB_ENDPOINT = config.get('omdb', 'endpoint')
    properties.OMDB_KEY = config.get('omdb', 'key')

    properties.GOOGLE_ENDPOINT = config.get('google', 'endpoint')
    properties.GOOGLE_KEY = config.get('google', 'key')
    properties.GOOGLE_CX = config.get('google', 'cx')

    return properties


CONFIG = load_properties()


def load_database():
    connection = MongoClient(CONFIG.DATABASE_ENDPOINT)
    return connection.dev


db = load_database()
