import services.movie_service as ms
from configs.config import db
from models.movie import Movie
from models.schedule import Schedule
from bson.json_util import dumps
import json

if __name__ == '__main__':
    candidates_json = json.loads(dumps(db.candidate.find({})))
    for candidate_json in candidates_json:
        candidate = Movie(candidate_json)
        found = db.movie.find_one({'sapo_id': candidate.sapo_id})
        if found is None:
            print('candidate')
            print(candidate)
            db.candidate.remove({'sapo_id': candidate.sapo_id})
            db.schedule.remove({'sapo_id': candidate.sapo_id})

    schedules_json = json.loads(dumps(db.schedule.find({})))
    for schedule_json in schedules_json:
        schedule = Schedule(schedule_json)
        found = db.movie.find_one({'sapo_id': schedule.sapo_id})
        if found is None:
            print('schedule')
            print(schedule)
            db.candidate.remove({'sapo_id': schedule.sapo_id})
            db.schedule.remove({'sapo_id': schedule.sapo_id})

    # movies_json = json.loads(dumps(db.movies.find({})))
    # for movie_json in movies_json:
    #     movie = Movie(movie_json)
    #     found = db.movie.find_one({'imdb_id': movie.imdb_id, 'sapo_id': {'$ne': movie.sapo_id}})
    #     if found is None:
    #         print('duplicated movie')
    #         print(found)
    #         print(movie)
            # db.candidate.remove({'sapo_id': schedule.sapo_id})
            # db.schedule.remove({'sapo_id': schedule.sapo_id})

    # corrupted_movies = json.loads(dumps(db.movie.find({'imdb_title': '()'})))
    # for corrupted_movie in corrupted_movies:
    #     candidate = Movie(corrupted_movie)
    #     candidate.imdb_id = candidate.imdb_id.replace('\n', '')
    #     ms.complete_movie_with_omdb(candidate)
    #     candidate.imdb_title = candidate.title + '(' + candidate.year + ')'
    #     ms.replace_movie(candidate)