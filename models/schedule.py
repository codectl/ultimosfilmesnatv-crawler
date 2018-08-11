class Schedule:

    def __init__(self):
        self.sapo_id = ''
        self.sapo_channel = ''
        self.sapo_start_datetime = ''
        self.sapo_end_datetime = ''
        self.sapo_duration = ''

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
