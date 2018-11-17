import json
import re
from bson import json_util


class Movie:

    def __init__(self, json_obj=None):
        if json_obj is None:
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
            self.alias_ids = []
            self.alias_titles = []
            self.isresolved = False
            self.nocandidates = False
            self.score = 0
        else:
            for key, value in json_obj.items():
                self.__dict__[key] = value

    @classmethod
    def from_pymongo(cls, obj):
        if obj is not None:
            serialized = json_util.loads(json_util.dumps(obj))
            if isinstance(serialized, list):
                return list(map(lambda e: Movie(e), serialized))
            return Movie(serialized)
        return None

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
        """Extracts actors from IMDb description"""
        description = self.imdb_description.strip()
        if description.split(' ')[0] == 'Directed':
            description = description.replace(self.director, '', 1).split('.')[1].strip()
        if description.split(' ')[0] == 'With':
            return description.split(' ', 1)[1].strip()
        return ''

    def combine_all_actors(self):
        """Combine all actors from IMDb and OMDb with no duplicates"""
        extracted_actors = self.extract_actors()
        return list(set(
            map(lambda e: e.strip(), extracted_actors.split(',')) if extracted_actors else [] + self.actors.split(',')))

    def evaluate_candidate_title(self):
        """Checks whether candidate title contains useful information"""
        matches = []
        if self.year in self.sapo_title:  # Checking year in title
            matches.append(('year', self.year))

        for word in self.imdb_title.split(' '):  # Check whether title has digits. Useful for volumes
            if word.isdigit() and word in self.sapo_title:
                matches.append(('saga', self.sapo_title))

        return matches

    def evaluate_candidate_description(self):
        """Checks whether candidate description contains useful information"""
        matches = []
        actors = self.combine_all_actors()
        for actor in actors:
            if actor in self.sapo_description:  # Checking actor
                matches.append(('description actor', actor))

        if self.director in self.sapo_description:  # Checking director
            matches.append(('description director', self.director))

        for entity in self._extract_entities_from_description():
            if entity.lower() in self.plot.lower():  # Checking entities
                matches.append(('description entity', entity))

        return matches

    def _extract_entities_from_description(self):
        """Extracting information from sapo description"""
        words = self.sapo_description.strip().split(' ')
        entities = []
        append = False
        substring = ''
        for word in words:
            if word and word[0].isupper() and (len(word) > 2 or (len(word) <= 2 and append)):
                if any(c == word[-1] for c in '(),.\'"'):
                    entities.append(substring.strip() + ' ' + word[:-1])
                    append = False
                    substring = ''
                else:
                    substring += ' ' + word
                    append = True
            elif re.match('[1-3][0-9]{3}', re.sub('[(),.\'"]', '', word)):  # Checking whether it is an year
                entities.append(re.sub('[(),.\'"]', '', word))
                append = False
                substring = ''
            elif append:
                entities.append(substring.strip())
                append = False
                substring = ''
        return entities

    def set_score(self, rules, movie):
        """Getting score for a certain candidate movie"""
        score = 0
        for rule in rules:
            if rule[0] == 'imdb link':
                score += 6
            elif rule[0] == 'imdb title':
                score += 2
            elif rule[0] == 'saga':
                score += 3
            elif rule[0] == 'actors':
                score += 4
            elif rule[0] == 'description':
                score += 1
            elif rule[0] == 'year':
                score += 5
            elif rule[0] == 'director':
                score += 4
            elif rule[0] == 'description actor':
                score += 4
            elif rule[0] == 'description director':
                score += 5
            elif rule[0] == 'description entity':
                score += 2
            elif rule[0] == 'best guess':
                score += 2

        if self.title == movie.sapo_title:
            score += 4

        self.score = score

    def to_dict(self):
        return json_util.loads(json_util.dumps(self.__dict__))
