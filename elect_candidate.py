import services.movie_service as ms
from models.movie import Movie
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("sapo_id", nargs='?', default="check_string_for_empty")
    parser.add_argument("imdb_id", nargs='?', default="check_string_for_empty")
    args = parser.parse_args()

    if args.sapo_id == 'check_string_for_empty':
        print('No argument given for sapo_id')
    elif args.imdb_id == 'check_string_for_empty':
        print('No argument given for imdb_id')
    else:
        movie = Movie(ms.get_movie_in_db_by_id(args.sapo_id))
        movie.imdb_id = args.imdb_id
        ms.complete_movie_with_omdb(movie)  # Complete movie with IMDB information
        movie.imdb_title = movie.title + '(' + movie.year + ')'
        movie.isresolved = True
        ms.replace_movie(movie)
        ms.delete_candidates(movie.sapo_id)  # Delete remaining candidates
