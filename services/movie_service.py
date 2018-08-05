import json
import urllib
from configs.config import CONFIG
from models.movie import Movie


def get_candidates(movie):
    query = movie.sapo_title.encode('utf8') + ' imdb'
    params = {
        'key': CONFIG.GOOGLE_KEY,
        'cx': CONFIG.GOOGLE_CX,
        'q': query
    }
    url = CONFIG.GOOGLE_ENDPOINT + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

    candidates = []

    print url

    for item in response['items']:
        if 'pagemap' in item and 'movie' in item['pagemap'] is not None:
            for movie_entry in item['pagemap']['movie']:
                if 'description' in movie_entry and \
                        not _exists_candidate(candidates, movie_entry['name']):
                    candidate = Movie()
                    candidate.imdb_id = _extract_imdb_id(item['link'])
                    candidate.imdb_title = movie_entry['name']
                    candidate.imdb_description = movie_entry['description']

                    candidates.append(candidate)

    return candidates


# Save movie into database after all relevent info is filled in
# TODO
def save_movie(movie, imdb_id):
    params = {
        'key': CONFIG.OMDB_KEY,
        'i': imdb_id
    }
    url = CONFIG.OMDB_ENDPOINT + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

    print response


# Adding movie to the unresolved movies in the database
# TODO
def mark_movie_as_unresolved(movie, additional_info):
    db = CONFIG.DATABASE_ENDPOINT


# Checking whether certain movie is already present in the candidates list
def _exists_candidate(candidates, name):
    for candidate in candidates:
        if candidate.imdb_title == name:
            return True
    return False


# Extracting IMDB title ID
def _extract_imdb_id(link):
    return link.replace('https://www.imdb.com/title', '').replace('/', '')
