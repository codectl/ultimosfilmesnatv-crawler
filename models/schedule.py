import json


class Schedule:

    def __init__(self):
        self.sapo_id = ''
        self.sapo_channel = ''
        self.sapo_start_datetime = ''
        self.sapo_end_datetime = ''
        self.sapo_duration = ''

    def __str__(self):
        return \
            '\n' + \
            '### ' + self.sapo_id + ' ###\n' + \
            'Sapo channel: ' + self.sapo_channel + '\n' + \
            'Sapo start datetime: ' + self.sapo_start_datetime + '\n' + \
            'Sapo start endtime: ' + self.sapo_end_datetime + '\n' + \
            'Sapo duration: ' + self.sapo_duration + '\n'

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
