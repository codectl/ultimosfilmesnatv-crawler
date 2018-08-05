import json
import urllib
from configs.config import CONFIG
from models.movie import Movie


def get_candidates(movie):
    query = movie.title_sapo.encode('utf8') + ' imdb'
    params = {
        'key': CONFIG.GOOGLE_KEY,
        'cx': CONFIG.GOOGLE_CX,
        'q': query
    }
    url = CONFIG.GOOGLE_ENDPOINT + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

    candidates = []

    for item in response['items']:
        if 'pagemap' in item and 'movie' in item['pagemap'] is not None:
            for movie_entry in item['pagemap']['movie']:
                if movie_entry['description'] is not None and \
                        _exists_candidate(candidates, movie_entry['name']):
                    candidate = Movie()
                    candidate.imdb_id = _extract_imdb_id(item['pagemap']['link'])
                    candidate.imdb_title = movie_entry['name']
                    candidate.imdb_description = movie_entry['description']

                    candidates.append(candidate)

    return candidates


# Save movie into database after all relevent info is filled in
# TODO
def save_movie(movie, additional_info):
    pass


# Adding movie to the unresolved movies in the database
# TODO
def mark_movie_as_unresolved(movie, additional_info):
    pass


# Checking whether certain movie is already present in the candidates list
def _exists_candidate(candidates, name):
    for candidate in candidates:
        if candidate.name == name:
            return True
    return False


# Extracting IMDB title ID
def _extract_imdb_id(link):
    return link.replace('https://www.imdb.com/title').replace('/')
