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
    return urllib.urlopen(url).read()


if __name__ == '__main__':
    # Getting daily epg for all channels
    response = request_daily_epg(u'AXN')

    # Parsing performed sapo request
    movies, schedules = epgparser.parse(response)

    for movie in movies:
        candidates = ms.get_candidates(movie)

        if not candidates:
            raise Exception('No candidates found')
        elif len(candidates) == 1:
            ms.save_movie(movie, candidates.pop())
        else:
            ms.mark_movie_as_unresolved(movie, candidates)
