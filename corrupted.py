import services.movie_service as ms
from configs.config import db
from models.movie import Movie
from models.schedule import Schedule
import json
from bson import json_util
import datetime

if __name__ == '__main__':
    # candidates_json = json.loads(dumps(db.candidate.find({})))
    # for candidate_json in candidates_json:
    #     candidate = Movie(candidate_json)
    #     found = db.movie.find_one({'sapo_id': candidate.sapo_id})
    #     if found is None:
    #         print('candidate')
    #         print(candidate)
    #         db.candidate.remove({'sapo_id': candidate.sapo_id})
    #         db.schedule.remove({'sapo_id': candidate.sapo_id})

    # schedules_json = json.loads(json_util.dumps(db.schedule.find({})), object_hook=json_util.object_hook)
    # for schedule_json in schedules_json:
    #     schedule = Schedule(schedule_json)
    #
    #     if isinstance(schedule.sapo_start_datetime, str):
    #
    #         sapo_start_datetime = datetime.datetime.strptime(schedule.sapo_start_datetime, '%Y-%m-%d %H:%M:%S')
    #
    #         try:
    #             sapo_duration = int(schedule.sapo_end_datetime)
    #             sapo_end_datetime = sapo_start_datetime + datetime.timedelta(seconds=sapo_duration)
    #             sapo_duration = str(sapo_duration)
    #         except:
    #             sapo_end_datetime = datetime.datetime.strptime(schedule.sapo_end_datetime, '%Y-%m-%d %H:%M:%S')
    #
    #         if 'duration' in schedule_json:
    #             sapo_duration = schedule_json['duration']
    #
    #         if not sapo_duration:
    #             raise Exception('Invalid option')
    #         else:
    #             if 'duration' in schedule_json:
    #                 db.schedule.update({'_id': schedule._id}, {'$unset': {'duration': ""}})
    #             # print(sapo_start_datetime)
    #             # print(sapo_end_datetime)
    #             # print(sapo_duration)
    #             db.schedule.update({'_id': schedule._id}, {'$set': {'sapo_start_datetime': sapo_start_datetime}})
    #             db.schedule.update({'_id': schedule._id}, {'$set': {'sapo_end_datetime': sapo_end_datetime}})
    #             db.schedule.update({'_id': schedule._id}, {'$set': {'sapo_duration': sapo_duration}})

    schedule = Schedule()
    schedule.sapo_id = '123'
    schedule.sapo_channel = 'ABC'
    schedule.sapo_start_datetime = datetime.datetime.now()
    schedule.sapo_end_datetime = datetime.datetime.now()
    schedule.sapo_duration = '12345'

    serialized = json_util.loads(json_util.dumps(schedule.__dict__))
    print(serialized)
    # db.schedule.insert(serialized)
    s = Schedule(json.loads(json_util.dumps(db.schedule.find_one({'sapo_id': schedule.sapo_id})), object_hook=json_util.object_hook))
    print(ms.exists_schedule_in_db(s.sapo_id, s.sapo_channel, s.sapo_start_datetime))

# found = db.movie.find_one({'sapo_id': schedule.sapo_id})
        # if found is None:
        #     print('schedule')
        #     print(schedule)
        # db.candidate.remove({'sapo_id': schedule.sapo_id})
        # db.schedule.remove({'sapo_id': schedule.sapo_id})

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
    #     candidate.imdb_title = candidate.title + ' (' + candidate.year + ')'
    #     ms.replace_movie(candidate)