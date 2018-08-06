import json
import urllib
from configs.config import CONFIG, db
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

    for item in response['items']:
        if 'pagemap' in item and 'movie' in item['pagemap'] is not None:
            for movie_entry in item['pagemap']['movie']:
                if 'description' in movie_entry and \
                        'imdb' in item['link'] and \
                        not _exists_candidate(candidates, movie_entry['name']):
                    candidate = Movie()
                    candidate.imdb_id = _extract_imdb_id(item['link'])
                    candidate.imdb_title = movie_entry['name']
                    candidate.imdb_description = movie_entry['description']

                    candidates.append(candidate)

    return candidates


# Save movie into database after all relevant info is filled in
# TODO
def save_movie(movie, candidate):
    params = {
        'apikey': CONFIG.OMDB_KEY,
        'i': candidate.imdb_id
    }
    url = CONFIG.OMDB_ENDPOINT + '?' + urllib.urlencode(params)
    print url
    response = json.loads(urllib.urlopen(url).read())

    movie.imdb_id = candidate.imdb_id
    movie.imdb_title = candidate.imdb_title
    movie.imdb_description = candidate.imdb_description
    movie.title = response['Title']
    movie.year = response['Year']
    movie.rated = response['Rated']
    movie.released = response['Released']
    movie.duration = response['Runtime']
    movie.genre = response['Genre']
    movie.director = response['Director']
    movie.writer = response['Writer']
    movie.actors = response['Actors']
    movie.plot = response['Plot']
    movie.language = response['Language']
    movie.country = response['Country']
    movie.awards = response['Awards']
    movie.poster = response['Poster']
    movie.rating_imdb = response['imdbRating']
    movie.rating_rotten_tomatoes = next(rating for rating in response['Ratings'] if rating['Source'] == 'Rotten Tomatoes')['Value']
    movie.rating_metacritic = response['Metascore']
    movie.website = response['Website']
    movie.iscomplete = True

    db.movie.insert(movie) # Store movie in database


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
