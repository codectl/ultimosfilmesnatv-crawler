
SAPO_ENDPOINT = u'http://services.sapo.pt/EPG/GetChannelByDateInterval?channelSigla={}&startDate={}&endDate={}'
OMDB_KEY = u'4f225d4b'
OMDB_BY_ID = u'http://www.omdbapi.com/?i={}'
OMDB_BY_TITLE = u'http://www.omdbapi.com/?t={}'

import datetime
import requests

if __name__ == '__main__':
  start = datetime.datetime.now()
  end =  start + datetime.timedelta(days=1)

  today_start = start.strftime(u'%Y-%m-%d') + u'+00:00:00'
  today_end = end.strftime(u'%Y-%m-%d') + u'+00:00:00'

  url = SAPO_ENDPOINT.format(u'AXN', today_start, today_end)
  response = requests.get(SAPO_ENDPOINT)

  print url
  print response
