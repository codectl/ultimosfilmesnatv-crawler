import json


class Movie:

    def __init__(self):
        self.sapo_id = ''
        self.sapo_title = ''
        self.sapo_description = ''
        self.imdb_id = ''
        self.imdb_title = ''
        self.imdb_description = ''
        self.title = ''
        self.year = ''
        self.rated = ''
        self.released = ''
        self.duration = ''
        self.genre = ''
        self.director = ''
        self.writer = ''
        self.actors = ''
        self.plot = ''
        self.language = ''
        self.country = ''
        self.awards = ''
        self.poster = ''
        self.rating_imdb = ''
        self.rating_rotten_tomatoes = ''
        self.rating_metacritic = ''
        self.website = ''
        self.isresolved = False

    def __str__(self):
        return \
            '\n' + \
            '### ' + self.sapo_id.encode('utf8') + ' ###\n' + \
            'Sapo title: ' + self.sapo_title.encode('utf8') + '\n' + \
            'Sapo description: ' + self.sapo_description.encode('utf8') + '\n' + \
            'Imdb id: ' + self.imdb_id.encode('utf8') + '\n' + \
            'Imdb title: ' + self.imdb_title.encode('utf8') + '\n' + \
            'Imdb description: ' + self.imdb_description.encode('utf8') + '\n' + \
            'Title: ' + self.title.encode('utf8') + '\n' + \
            'Year: ' + self.year.encode('utf8') + '\n' + \
            'Plot: ' + self.plot.encode('utf8') + '\n' + \
            'Genre: ' + self.genre.encode('utf8') + '\n' + \
            'Actors: ' + self.actors.encode('utf8') + '\n' + \
            'IsResolved?: ' + str(self.isresolved) + '\n'

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
