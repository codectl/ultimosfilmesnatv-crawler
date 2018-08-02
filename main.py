
SAPO_ENDPOINT = u'http://services.sapo.pt/EPG/GetChannelByDateInterval?channelSigla={}&startDate={}&endDate={}'
OMDB_KEY = u'4f225d4b'
OMDB_BY_ID = u'http://www.omdbapi.com/?i={}'
OMDB_BY_TITLE = u'http://www.omdbapi.com/?t={}'

import datetime
import requests
import services.sapo_parser as epgparser

def request_daily_epg(channel):
  start = datetime.datetime.now()
  end =  start + datetime.timedelta(days=1)

  today_start = start.strftime(u'%Y-%m-%d') + u'+00:00:00'
  today_end = end.strftime(u'%Y-%m-%d') + u'+00:00:00'

  url = SAPO_ENDPOINT.format(channel, today_start, today_end)
  response = requests.get(url)

  return response.text


if __name__ == '__main__':

  # Getting daily epg for all channels
  response = request_daily_epg(u'AXN')

  # Parsing performed sapo request
  movies, schedules = epgparser.parse(response)

  print movies
