import datetime
import requests
import services.sapo_parser as epgparser
from configs.config import CONFIG


def request_daily_epg(channel):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=1)

    today_start = start.strftime(u'%Y-%m-%d') + u'+00:00:00'
    today_end = end.strftime(u'%Y-%m-%d') + u'+00:00:00'

    url = CONFIG.SAPO_ENDPOINT.format(channel, today_start, today_end)
    response = requests.get(url)

    return response.text


if __name__ == '__main__':
    # Getting daily epg for all channels
    response = request_daily_epg(u'AXN')

    # Parsing performed sapo request
    movies, schedules = epgparser.parse(response)
