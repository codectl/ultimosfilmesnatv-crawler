import datetime
import urllib
import services.sapo_parser as epgparser
import services.movie_service as ms
from configs.config import CONFIG


def request_daily_epg(channel):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=1)

    today_start = start.strftime(u'%Y-%m-%d') + u' 00:00:00'
    today_end = end.strftime(u'%Y-%m-%d') + u' 00:00:00'

    params = [
        ('channelSigla', channel),
        ('startDate', today_start),
        ('endDate', today_end)
    ]
    url = CONFIG.SAPO_ENDPOINT + '?' + urllib.urlencode(params)
    print url
    return urllib.urlopen(url).read()


if __name__ == '__main__':
    # Getting daily epg for all channels
    response = request_daily_epg(u'AXN')

    # Parsing performed sapo request
    movies, schedules = epgparser.parse(response)

    for movie in movies:
        candidates = ms.get_candidates(movie)

        print '\n ****'
        print movie.sapo_title
        print movie.sapo_description

        print candidates
        for c in candidates:
            print c.imdb_title
            print c.imdb_description

        if not candidates:
            raise Exception('No candidates found for movie {}'.format(movie.sapo_title.encode('utf8')))
        elif len(candidates) == 1:
            ms.save_movie(ms.complete_movie(movie, candidates.pop()))
        else:
            ms.mark_movie_as_unresolved(movie, candidates)
