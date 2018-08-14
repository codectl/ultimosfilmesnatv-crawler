import json
import urllib, urllib.request
from configs.config import CONFIG, db
from models.movie import Movie
import uuid


def get_candidates(movie):
    query = movie.sapo_title + ' imdb'
    params = {
        'key': CONFIG.GOOGLE_KEY,
        'cx': CONFIG.GOOGLE_CX,
        'q': query
    }
    url = CONFIG.GOOGLE_ENDPOINT + '?' + urllib.parse.urlencode(params)
    response = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))

    candidates = []

    for item in response['items']:
        if 'pagemap' in item and 'movie' in item['pagemap'] is not None:
            for movie_entry in item['pagemap']['movie']:
                if 'description' in movie_entry and \
                        'imdb' in item['link'] and \
                        not _exists_candidate(candidates, movie_entry['name']):
                    candidate = Movie()
                    candidate.sapo_id = movie.sapo_id
                    candidate.sapo_title = movie.sapo_title
                    candidate.sapo_description = movie.sapo_description
                    candidate.imdb_id = _extract_imdb_id(item['link'])
                    candidate.imdb_title = movie_entry['name']
                    candidate.imdb_description = movie_entry['description']
                    complete_movie_with_omdb(candidate)  # Adding further attributes to the movie object

                    candidates.append(candidate)

    return candidates


#  Fill all relevant info of a movie
def complete_movie_with_omdb(movie):
    params = {
        'apikey': CONFIG.OMDB_KEY,
        'i': movie.imdb_id
    }
    url = CONFIG.OMDB_ENDPOINT + '?' + urllib.parse.urlencode(params)
    print(url)
    response = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))

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
    movie.rating_rotten_tomatoes = \
        next((rating for rating in response['Ratings'] if rating['Source'] == 'Rotten Tomatoes'), {'Value': ''})[
            'Value']
    movie.rating_metacritic = response['Metascore']
    movie.website = response['Website']


# Save movie into database
def save_movie(movie):
    movie_json = json.loads(movie.to_json())
    movie_json['_id'] = uuid.uuid1()
    db.movie.insert(movie_json)


# Replacing movie entry with the new one
def replace_movie(movie):
    db.movie.delete_one({'sapo_id': movie.sapo_id})
    save_movie(movie)


# Save schedule into database
def save_schedule(schedule):
    db.schedule.insert(json.loads(schedule.to_json()))


# Check whether a movie already exists in database given its ID
def exists_movie_in_db(sapo_id):
    return db.movie.find({'sapo_id': sapo_id}).count() != 0


# Check whether a schedule already exists in database
def exists_schedule_in_db(sapo_id, sapo_channel, sapo_start_datetime):
    return db.schedule.find({
        'sapo_id': sapo_id,
        'sapo_channel': sapo_channel,
        'sapo_start_datetime': sapo_start_datetime
    }).count() != 0


# Add movie to the unresolved movies in the database
def save_candidates(candidates):
    for candidate in candidates:
        db.candidate.insert(json.loads(candidate.to_json()))  # Store unresolved entry in database


# Delete candidate movies
def delete_candidates(sapo_id):
    db.candidate.delete_many({'sapo_id': sapo_id})


# Get list of unresolved movies
def get_all_unresolved_movies():
    return db.movie.find({'isresolved': False})


# Getting list of unresolved movies
def get_all_candidates(sapo_id):
    return db.candidate.find({'sapo_id': sapo_id})


# Checking whether certain movie is already present in the candidates list
def _exists_candidate(candidates, name):
    for candidate in candidates:
        if candidate.imdb_title == name:
            return True
    return False


# Extracting IMDB title ID
def _extract_imdb_id(link):
    return link.replace('https://www.imdb.com/title', '').replace('/', '')
