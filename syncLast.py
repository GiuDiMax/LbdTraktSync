from lbdConfig import getLetterboxdHeader, letterboxdbaseurl, lbduid
from traktConfig import getTraktHeaders, traktbaseurl
import requests
from datetime import datetime as dt


def syncLast():
    global lastentry
    x = {}
    tmdb = 0
    item = getLastActivity()
    x['type'] = ""
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
        d1 = dt.fromisoformat(getLastTrakt())
        d2 = dt.fromisoformat(item['diaryEntry']['whenCreated'])
        diff = abs((d1-d2).total_seconds())
        if diff >= 1800:
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


def getLastTrakt():
    #x = requests.get(traktbaseurl + f'/users/id/history?start_at={(datetime.now() - timedelta(days=1)).isoformat()}&end_at={datetime.now().isoformat()}', headers=getTraktHeaders()).json()
    return requests.get(traktbaseurl + '/sync/last_activities', headers=getTraktHeaders()).json()['movies']['watched_at']


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
