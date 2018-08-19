from configs.config import db
from models.movie import Movie
from bson.json_util import dumps
import json

if __name__ == '__main__':
    movies = json.loads(dumps(db.movie.find({})))
    for movie in movies:
        movie = Movie(movie)
        found = db.movie.find_one({'title': movie.title, 'year': movie.year, 'sapo_id': {'$ne': movie.sapo_id}})
        if found is not None:
            found = Movie(found)
            db.schedule.update({'sapo_id': found.sapo_id}, {'$set': {'sapo_id': movie.sapo_id}})
            db.candidate.remove({'sapo_id': found.sapo_id})
            db.movie.remove({'sapo_id': found.sapo_id})
            print(found.imdb_id)
            print(movie.imdb_id)
            print('***********')
