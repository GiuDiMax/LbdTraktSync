from lbdConfig import getLetterboxdHeader, letterboxdbaseurl, lbduid
from traktConfig import getTraktHeaders, traktbaseurl
import requests
from datetime import datetime


def syncLast():
    x = {}
    tmdb = 0
    item = getLastActivity()
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
        date = datetime.strptime(item['diaryEntry']['diaryDetails']['diaryDate'], '%Y-%m-%d')
        for link in item['diaryEntry']['film']['links']:
            if link['type'] == 'tmdb':
                tmdb = link['id']
                break
        if tmdb == 0:
            x['error'] = "no tmdb code"
            return x
        if date.day == datetime.today().day:
            movie = {"movies": [{"watched_at": datetime.now().isoformat(), "ids": {"tmdb": tmdb}}]}
            x = requests.post(traktbaseurl + '/sync/history/', headers=getTraktHeaders(), json=movie).json()
        if 'rating' in item['diaryEntry']['film']['relationships'][0]['relationship']:
            rating = int(item['diaryEntry']['film']['relationships'][0]['relationship']['rating'] * 2)
            movie = {"movies": [{"rating": rating, "ids": {"tmdb": tmdb}}]}
            y = requests.post(traktbaseurl + '/sync/ratings', headers=getTraktHeaders(), json=movie).json()
            if x == {}:
                x = y
    x['type'] = item['type']
    return x


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
    lastentry = item
    return item


if __name__ == '__main__':
    print(syncLast())
