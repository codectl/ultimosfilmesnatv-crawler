from configs.config import db
from models.movie import Movie
from bson.json_util import dumps
import json

if __name__ == '__main__':
    candidates = json.loads(dumps(db.candidate.find({})))
    for candidate in candidates:
        candidate = Movie(candidate)
        found = db.movie.find_one({'sapo_id': candidate.sapo_id})
        if found is None:
            db.candidate.remove({'sapo_id': candidate.sapo_id})
            db.schedule.remove({'sapo_id': candidate.sapo_id})

    schedules = json.loads(dumps(db.schedule.find({})))
    for schedule in schedules:
        schedule = Movie(schedule)
        found = db.movie.find_one({'sapo_id': schedule.sapo_id})
        if found is None:
            db.candidate.remove({'sapo_id': schedule.sapo_id})
            db.schedule.remove({'sapo_id': schedule.sapo_id})