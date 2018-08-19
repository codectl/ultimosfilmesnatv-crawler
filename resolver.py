import services.movie_service as ms
from models.movie import Movie
from bson.json_util import dumps
import json
import sys

if __name__ == '__main__':
    unresolved_movies_json = json.loads(dumps(ms.get_all_unresolved_movies()))

    # Solving each unresolved movie
    for unresolved_movie_json in unresolved_movies_json:
        unresolved_movie = Movie(unresolved_movie_json)  # Getting object from json

        print('\n')
        print('*** {} ***'.format(unresolved_movie.sapo_id))
        print('Movie sapo title: {}'.format(unresolved_movie.sapo_title))
        print('Movie sapo description: {}'.format(unresolved_movie.sapo_description))
        print('* Choose one of the following candidates *')

        # Electing the right candidate
        candidates_json = json.loads(dumps(ms.get_all_candidates(unresolved_movie.sapo_id)))
        candidates = []

        for index, candidate_json in enumerate(candidates_json, start=1):
            candidate = Movie(candidate_json)  # Getting object from json
            candidates.append(candidate)

            print('[{}] Title: {}'.format(index, candidate.imdb_title))
            print('    Year: {}'.format(candidate.year))
            print('    Description: {}'.format(candidate.plot))
            print('Chosen option: ')

        option = int(sys.stdin.readline())  # reading option from stdin
        elected = candidates[option - 1]
        elected.isresolved = True
        ms.replace_movie(elected)  # Replace movie with elected one
        ms.delete_candidates(unresolved_movie.sapo_id)  # Deleting all previous candidates
