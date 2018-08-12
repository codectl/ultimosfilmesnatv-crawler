import services.movie_service as ms
from bson.json_util import dumps
from models.movie import Movie
import json


if __name__ == '__main__':
    unresolved_movies_json = ms.get_all_unresolved_movies()

    # Solving each unresolved movie
    for unresolved_movie_json in json.loads(dumps(unresolved_movies_json)):
        unresolved_movie = Movie(unresolved_movie_json) # Getting object from json

        candidates_json = ms.get_all_candidates(unresolved_movie.sapo_id)

        print('\n')
        print('***')
        print('Movie sapo title: {}'.format(unresolved_movie.sapo_title))
        print('Movie sapo description: {}'.format(unresolved_movie.sapo_description))

        # Electing the right candidate
        for index, candidate_json in enumerate(json.loads(dumps(candidates_json)), start=1):
            candidate = Movie(candidate_json) # Getting object from json

            print('[{}] Title: {}'.format(index, candidate.imdb_title))
            print('    Description: {}'.format(candidate.imdb_description))
