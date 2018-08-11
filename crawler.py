import datetime
import urllib, urllib.request
import services.sapo_parser as epgparser
import services.movie_service as ms
from configs.config import CONFIG


def request_daily_epg(channel):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=1)

    today_start = start.strftime('%Y-%m-%d') + ' 00:00:00'
    today_end = end.strftime('%Y-%m-%d') + ' 00:00:00'

    params = [
        ('channelSigla', channel),
        ('startDate', today_start),
        ('endDate', today_end)
    ]
    url = CONFIG.SAPO_ENDPOINT + '?' + urllib.parse.urlencode(params)
    print(url)
    return urllib.request.urlopen(url).read().decode('utf-8')


if __name__ == '__main__':
    # Getting daily epg for all channels
    response = request_daily_epg('AXN')

    # Parsing performed sapo request
    movies, schedules = epgparser.parse(response)

    # Persist each movie
    for movie in movies:

        if not ms.exists_movie_in_db(movie.sapo_id):

            candidates = ms.get_candidates(movie)

            print('\n ****')
            print(movie.sapo_title)
            print(movie.sapo_description)

            print(candidates)
            for c in candidates:
                print (c.imdb_title)
                print (c.imdb_description)

            if not candidates:
                raise Exception('No candidates found for movie {}'.format(movie.sapo_title))
            elif len(candidates) == 1:
                unsaved_movie = ms.complete_movie(movie, candidates.pop())
                ms.save_movie(unsaved_movie)
            else:
                ms.save_candidates(movie, candidates)
                ms.save_movie(movie)

        else:
            print("Movie already exists")

    # Persist each schedule
    for schedule in schedules:
        if not ms.exists_schedule_in_db(schedule.sapo_id, schedule.sapo_channel, schedule.sapo_start_datetime):
            ms.save_schedule(schedule)
