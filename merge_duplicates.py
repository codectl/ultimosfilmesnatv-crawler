import services.movie_service as ms
from models.movie import Movie
from configs.config import db
from bson.json_util import dumps
import argparse
import json
import sys

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

                print('\n')
                print('*** IMDb movie ID: {} ***'.format(movie.imdb_id))
                print('[1] Sapo ID: {}'.format(movie.sapo_id))
                print('    Sapo title: {}. IMDb title: {}'.format(movie.sapo_title, movie.imdb_title))
                print('    Sapo Description: {}'.format(movie.sapo_description))
                print('    IMDb Description: {}'.format(movie.imdb_description))

                print('\n')
                print('[2] Sapo ID: {}'.format(found.sapo_id))
                print('    Sapo title: {}. IMDb title: {}'.format(found.sapo_title, found.imdb_title))
                print('    Sapo Description: {}'.format(found.sapo_description))
                print('    IMDb Description: {}'.format(found.imdb_description))

                print('\n')
                print('* Which one to keep? *')

                option = int(sys.stdin.readline())

                if option == 1:
                    keep = movie
                    replace = found
                elif option == 2:
                    keep = found
                    replace = movie
                else:
                    raise Exception('Invalid option')

                db.schedule.update({'sapo_id': replace.sapo_id}, {'$set': {'sapo_id': keep.sapo_id}})
                db.candidate.update({'sapo_id': replace.sapo_id}, {'$set': {'sapo_id': keep.sapo_id}})
                db.movie.remove({'sapo_id': replace.sapo_id})
