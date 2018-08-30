import json
import re


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
            self.score = 0
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

    def get_description_sapo_matches(self):
        """Checks whether sapo description contains useful information"""
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
            if word[0].isupper() and (len(word) > 2 or (len(word) <= 2 and append)):
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

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
