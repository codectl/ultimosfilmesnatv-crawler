import json


class Movie:

    def __init__(self, json_obj=None):
        if json_obj == None:
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
            self.nocandidates = False
        else:
            for key, value in json_obj.items():
                self.__dict__[key] = value

    def __str__(self):
        return \
            '\n' + \
            '### ' + self.sapo_id + ' ###\n' + \
            'Sapo title: ' + self.sapo_title + '\n' + \
            'Sapo description: ' + self.sapo_description + '\n' + \
            'Imdb id: ' + self.imdb_id + '\n' + \
            'Imdb title: ' + self.imdb_title + '\n' + \
            'Imdb description: ' + self.imdb_description + '\n' + \
            'Title: ' + self.title + '\n' + \
            'Year: ' + self.year + '\n' + \
            'Plot: ' + self.plot + '\n' + \
            'Genre: ' + self.genre + '\n' + \
            'Actors: ' + self.actors + '\n' + \
            'IsResolved?: ' + str(self.isresolved) + '\n'

    def extract_actors(self):
        """Extracting actors from IMDb description"""
        description = self.imdb_description
        if description.split(' ')[0].strip() == 'Directed':
            description = description.split('.')[1]
        if description.split(' ')[0].strip() == 'With':
            return description.split(' ')[1].strip().split('.')[0]
        return ''

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
