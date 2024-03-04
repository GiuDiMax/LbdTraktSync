from lbdConfig import getLetterboxdHeader, letterboxdbaseurl, lbduid
from traktConfig import getTraktHeaders, traktbaseurl
import requests
from datetime import datetime
from dateutil.parser import parse


def syncLast():
    global lastentry
    x = {}
    tmdb = 0
    item = getLastActivity()
    x['type'] = ""
    sync = False
    if item is None:
        x['type'] = "no new activities"
        return
    if item['type'] == 'FilmRatingActivity':
        for link in item['film']['links']:
            if link['type'] == 'tmdb':
                tmdb = link['id']
                break
        if tmdb == 0:
            x['error'] = "no tmdb code"
            return x
        rating = int(item['film']['relationships'][0]['relationship']['rating'] * 2)
        movie = {"movies": [{"rating": rating, "ids": {"tmdb": tmdb}}]}
        x = requests.post(traktbaseurl + '/sync/ratings', headers=getTraktHeaders(), json=movie).json()
    elif item['type'] == 'DiaryEntryActivity':
        for link in item['diaryEntry']['film']['links']:
            if link['type'] == 'tmdb':
                tmdb = link['id']
                break
        if tmdb == 0:
            x['error'] = "no tmdb code"
            return x
        r = getLastTrakt2(tmdb)
        if r == "error":
            return "error"
        if r == []:
            sync = True
        else:
            d1 = parse(r[0]['watched_at'])
            d2 = parse(item['diaryEntry']['whenCreated'])
            #print(d1)
            #print(d2)
            diff = abs((d1-d2).total_seconds())
            #print(diff)
            if diff >= 3600:
                sync = True
        if sync:
            movie = {"movies": [{"watched_at": item['diaryEntry']['whenCreated'], "ids": {"tmdb": tmdb}}]}
            x = requests.post(traktbaseurl + '/sync/history/', headers=getTraktHeaders(), json=movie).json()
            x['type'] = item['type']
        if 'rating' in item['diaryEntry']['film']['relationships'][0]['relationship']:
            rating = int(item['diaryEntry']['film']['relationships'][0]['relationship']['rating'] * 2)
            movie = {"movies": [{"rating": rating, "ids": {"tmdb": tmdb}}]}
            y = requests.post(traktbaseurl + '/sync/ratings', headers=getTraktHeaders(), json=movie).json()
            x['type'] = x['type'] + ' - FilmRatingActivity'
    lastentry = item
    return x


def getLastTrakt2(tmdb):
    result = requests.get(traktbaseurl + '/search/tmdb/'+str(tmdb)+'?type=movie', headers=getTraktHeaders()).json()
    if 'movie' in result[0]:
        trakt = result[0]['movie']['ids']['trakt']
        result = requests.get(traktbaseurl + '/sync/history/movies/' + str(trakt), headers=getTraktHeaders()).json()
        return result
    return "error"


def getLastTrakt():
    #x = requests.get(traktbaseurl + f'/users/id/history?start_at={(datetime.now() - timedelta(days=1)).isoformat()}&end_at={datetime.now().isoformat()}', headers=getTraktHeaders()).json()
    result = requests.get(traktbaseurl + '/sync/last_activities', headers=getTraktHeaders()).json()
    return result['movies']['watched_at']


def getLastActivity():
    global lastentry
    resp = requests.get(letterboxdbaseurl + f'/member/{lbduid}/activity?where=OwnActivity&include=DiaryEntryActivity&include=FilmRatingActivity', headers=getLetterboxdHeader()).json()
    if 'items' not in resp:
        return None
    if len(resp['items']) == 0:
        return None
    item = resp['items'][0]
    try:
        if item == lastentry:
            return None
    except:
        pass
    return item


if __name__ == '__main__':
    print(syncLast())
