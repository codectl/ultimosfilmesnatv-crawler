import services.movie_service as ms
from models.movie import Movie
from models.schedule import Schedule
from bson.json_util import dumps
import json
import sys
from PIL import Image
import urllib.request, io
import services.google_vision as im
from configs.config import CONFIG


def _print_img(uri):
    """Printing image"""
    file = io.BytesIO(urllib.request.urlopen(uri).read())
    image = Image.open(file)
    image.show()
    im.detect_web_uri(uri)


if __name__ == '__main__':
    unresolved_movies_json = json.loads(dumps(ms.get_all_unresolved_movies()))

    # Solving each unresolved movie
    for unresolved_movie_json in unresolved_movies_json:
        unresolved_movie = Movie(unresolved_movie_json)  # Getting object from json

        schedule = Schedule(json.loads(dumps(ms.get_channel_movie(unresolved_movie.sapo_id))))

        print('\n')
        print('*** {} *** [{}]'.format(unresolved_movie.sapo_id, schedule.sapo_channel))
        print('Movie sapo title: {}'.format(unresolved_movie.sapo_title))
        print('Movie sapo description: {}'.format(unresolved_movie.sapo_description))
        print('* Choose one of the following candidates *')

        img_uri = CONFIG.SAPO_IMAGE.format(unresolved_movie.sapo_id)
        _print_img(img_uri)  # Printing movie image
        annotations = im.detect_web_uri(img_uri)  # Getting nnotation from Google Vision API

        # Electing the right candidate
        candidates_json = json.loads(dumps(ms.get_all_candidates(unresolved_movie.sapo_id)))
        candidates = []

        for candidate_json in candidates_json:
            candidate = Movie(candidate_json)  # Getting object from json
            candidates.append((candidate, im.evaluate_candidate(annotations, candidate)))

        candidates.sort(key=lambda tuple: len(tuple[1]), reverse=True)  # Sorting by number of matches

        for index, (candidate, matches) in enumerate(candidates, start=1):
            print('\n')
            print('[{}] Title: {} - {}'.format(index, candidate.imdb_title, candidate.imdb_id))
            print('    OMDB Description: {}'.format(candidate.plot))
            print('    IMDb Description: {}'.format(candidate.imdb_description))
            print('    Actors: {}'.format(candidate.actors))
            print('    Matches: {} - {}'.format(len(matches), matches))

        # Additional candidates to include in movie selection
        additional_candidates = im.google_vision_candidates(annotations, [tuple[0] for tuple in candidates])
        if len(additional_candidates) > 0:
            print('\n')
            print('Additional candidates found')
            for additional_candidate in additional_candidates:
                print(additional_candidate)

        print('Chosen option: ')
        option = sys.stdin.readline()  # reading option from stdin

        try:  # Check whether the input is an int
            option = int(option)
        except ValueError:
            if option[:2] == 'tt':  # Checking whether it is an IMDb ID
                unresolved_movie.imdb_id = option
                ms.complete_movie_with_omdb(unresolved_movie)
                unresolved_movie.imdb_title = unresolved_movie.title + '(' + unresolved_movie.year + ')'
                unresolved_movie.isresolved = True
                ms.replace_movie(unresolved_movie)  # Replace old entry with updated one
                ms.delete_candidates(unresolved_movie.sapo_id)  # Delete candidates
            else:
                raise Exception('Invalid option')
        else:
            elected = candidates[option - 1][0]
            elected.isresolved = True
            ms.replace_movie(elected)  # Replace movie with elected one
            ms.delete_candidates(unresolved_movie.sapo_id)  # Deleting all previous candidates
