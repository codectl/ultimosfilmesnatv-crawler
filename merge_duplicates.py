import services.movie_service as ms
from models.movie import Movie
from configs.config import db
from bson.json_util import dumps
from difflib import SequenceMatcher
import json
import sys
import uuid

if __name__ == '__main__':
    movies = Movie.from_pymongo(db.movie.find({}))
    repeated = []
    for movie in movies:
        found = Movie.from_pymongo(
            db.movie.find_one({'imdb_title': movie.imdb_title, 'sapo_id': {'$ne': movie.sapo_id}}))
        if found is not None:
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
                print('Description similarity ratio: {}'.format(
                    SequenceMatcher(None, movie.sapo_description, found.sapo_description).ratio()))

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

                db.schedule.update_many({'sapo_id': replace.sapo_id}, {'$set': {'sapo_id': keep.sapo_id}})
                db.candidate.update({'sapo_id': replace.sapo_id}, {'$set': {'sapo_id': keep.sapo_id}})
                db.movie.update({'sapo_id': keep.sapo_id}, {'$push': {'alias_ids': replace.sapo_id}})
                if keep.sapo_title != replace.sapo_title:
                    db.movie.update({'sapo_id': keep.sapo_id}, {'$push': {'alias_titles': replace.sapo_title}})
                db.movie_aliases.update_many({'alias_of': replace.sapo_id}, {'$set': {'alias_of': keep.sapo_id}})
                if SequenceMatcher(None, keep.sapo_description, replace.sapo_description).ratio() <= 0.5:
                    db.movie_aliases.insert(
                        {'sapo_title': replace.sapo_title,
                         'sapo_description': replace.sapo_description,
                         'alias_of': keep.sapo_id})

                db.movie.remove({'sapo_id': replace.sapo_id})
