from lbdConfig import getLetterboxdHeader, letterboxdbaseurl, lbduid
import requests
from traktConfig import getTraktHeaders, traktbaseurl
from threading import Thread


def syncAll():
    total = []
    a = getLetterboxdRatings()
    print(len(a))
    b = getTraktRatings()
    print(len(b))
    for element in a:
        if element not in b:
            total.append(element)
    print(len(total))
    if total is None:
        return
    x = requests.post(traktbaseurl + '/sync/ratings', headers=getTraktHeaders(), json={'movies': total}).json()
    return x


def getTraktRatings():
    totale = []
    x = requests.get(traktbaseurl + '/sync/ratings/movies', headers=getTraktHeaders()).json()
    for item in x:
        if 'tmdb' not in item['movie']['ids']:
            continue
        totale.append({'tmdb': item['movie']['ids']['tmdb'], 'rating': item['rating']})
    return totale


def getLetterboxdRatings():
    headers = getLetterboxdHeader()
    cursor = 'start=0'
    totale = []
    while True:
        x = requests.get(letterboxdbaseurl + f'/films?perPage=100&where=Rated&where=Film&cursor={cursor}', headers=headers).json()
        for item in x['items']:
            f = {}
            for link in item['links']:
                if link['type'] == 'tmdb':
                    f['tmdb'] = link['id']
                    #f['ids'] = {'tmdb': link['id']}
                    break
            f['rating'] = int(item['relationships'][0]['relationship']['rating'] * 2)
            totale.append(f)
        if 'next' not in x:
            return totale
        cursor = x['next']


if __name__ == '__main__':
    print(syncAll())
