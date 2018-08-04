class Movie:

    def __init__(self):
        pass

    def __str__(self):
        return \
            '\n' + \
            '### ' + self.id_sapo.encode('utf8') + ' ###\n' + \
            'Title_sapo: ' + self.title_sapo.encode('utf8') + '\n' + \
            'Description_pt: ' + self.description_sapo.encode('utf8') + '\n' + \
            'Duration: ' + self.duration.encode('utf8') + '\n'
