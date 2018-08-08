from ConfigParser import ConfigParser
from pymongo import MongoClient


class Properties:
    def __init__(self):
        pass


def load_properties():
    # Read configuration properties
    config = ConfigParser()
    config.read(u'configs/properties.ini')

    properties = Properties()
    properties.DATABASE_ENDPOINT = config.get(u'database', u'endpoint')

    properties.SAPO_ENDPOINT = config.get(u'sapo', u'endpoint')
    properties.NS = config.get(u'sapo', u'ns')

    properties.OMDB_ENDPOINT = config.get(u'omdb', u'endpoint')
    properties.OMDB_KEY = config.get(u'omdb', u'key')

    properties.GOOGLE_ENDPOINT = config.get(u'google', u'endpoint')
    properties.GOOGLE_KEY = config.get(u'google', u'key')
    properties.GOOGLE_CX = config.get(u'google', u'cx')

    return properties


CONFIG = load_properties()


def load_database():
    connection = MongoClient(CONFIG.DATABASE_ENDPOINT)
    return connection.dev


db = load_database()
