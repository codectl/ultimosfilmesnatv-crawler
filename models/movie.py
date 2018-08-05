import json


class Movie:

    def __init__(self):
        self.sapo_id = ''
        self.sapo_title = ''
        self.sapo_description = ''
        self.imdb_id = ''
        self.imdb_title = ''
        self.imdb_description = ''
        self.complete = False

    def __str__(self):
        return \
            '\n' + \
            '### ' + self.sapo_id.encode('utf8') + ' ###\n' + \
            'Title_sapo: ' + self.sapo_title.encode('utf8') + '\n' + \
            'Description_pt: ' + self.sapo_description.encode('utf8') + '\n'

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
