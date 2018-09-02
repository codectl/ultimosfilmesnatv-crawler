from configs.config import db
from models.movie import Movie
from bson.json_util import dumps
import json

if __name__ == '__main__':
    movies = json.loads(dumps(db.movie.find({})))
    repeated = []
    for movie in movies:
        movie = Movie(movie)
        found = db.movie.find_one({'imdb_title': movie.imdb_title, 'sapo_id': {'$ne': movie.sapo_id}})
        if found is not None:
            found = Movie(found)
            if found.sapo_id not in repeated:
                repeated.append(movie.sapo_id)
                repeated.append(found.sapo_id)
                print(found.sapo_id)
                print(movie.sapo_id)
                print(found.sapo_title)
                print(movie.sapo_title)
                print('***********')

                # db.schedule.update({'sapo_id': found.sapo_id}, {'$set': {'sapo_id': movie.sapo_id}})
                # db.candidate.remove({'sapo_id': found.sapo_id})
                # db.movie.remove({'sapo_id': found.sapo_id})
