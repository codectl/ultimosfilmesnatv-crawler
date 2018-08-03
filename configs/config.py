from ConfigParser import ConfigParser

class Properties:
    pass

def load_properties():

    # Read configuration properties
    config = ConfigParser()
    config.read(u'configs/properties.ini')

    properties = Properties()
    properties.SAPO_ENDPOINT = config.get(u'sapo', u'endpoint')
    properties.NS = config.get(u'sapo', u'ns')

    properties.OMDB_KEY = config.get(u'omdb', u'key')
    properties.OMDB_BY_ID = config.get(u'omdb', u'by_id')
    properties.OMDB_BY_TITLE = config.get(u'omdb', u'by_title')

    return properties

CONFIG = load_properties()