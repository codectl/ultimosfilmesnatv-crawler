import services.movie_service as ms
from models.movie import Movie
from bson.json_util import dumps
import json
import sys
from PIL import Image
import urllib.request, io

if __name__ == '__main__':
    unresolved_movies_json = json.loads(dumps(ms.get_all_unresolved_movies()))

    # Solving each unresolved movie
    for unresolved_movie_json in unresolved_movies_json:
        unresolved_movie = Movie(unresolved_movie_json)  # Getting object from json

        img = 'http://services.online.meo.pt/Data/2013/11/programs/media/image/{}/L'.format(unresolved_movie.sapo_id)
        print(img)
        file = io.BytesIO(urllib.request.urlopen(img).read())
        image = Image.open(file)
        image.show()

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
            print('    OMDB Description: {}'.format(candidate.plot))
            print('    IMDb Description: {}'.format(candidate.imdb_description))
            print('    Actors: {}'.format(candidate.actors))
            print('Chosen option: ')

        option = sys.stdin.readline()  # reading option from stdin

        try: # Check whether the input is an int
            option = int(option)
        except ValueError:
            if option[:2] == 'tt': # Checking whether it is an IMDb ID 
                unresolved_movie.imdb_id = option
                ms.complete_movie_with_omdb(unresolved_movie)
                unresolved_movie.imdb_title = unresolved_movie.title + '(' + unresolved_movie.year + ')'
                unresolved_movie.isresolved = True
                ms.replace_movie(unresolved_movie) # Replace old entry with updated one
                ms.delete_candidates(unresolved_movie.sapo_id)  # Delete candidates
            else:
                raise Exception('Invalid option')
        else:
            elected = candidates[option - 1]
            elected.isresolved = True
            ms.replace_movie(elected)  # Replace movie with elected one
            ms.delete_candidates(unresolved_movie.sapo_id)  # Deleting all previous candidates            
                