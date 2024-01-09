from lbdConfig import getLetterboxdHeader, letterboxdbaseurl, lbduid, listid
import requests
from traktConfig import getTraktHeaders, traktbaseurl


def setWatchlist():
    a = set(getLbdWatchlist())
    b = set(getTraktWatchlist())
    toAdd = []
    toRemove = []
    for item in list(a - b):
        toAdd.append({'ids': {'tmdb': item}})
    for item in list(b - a):
        toRemove.append({'ids': {'tmdb': item}})
    x = requests.post(traktbaseurl + '/sync/watchlist', headers=getTraktHeaders(), json={'movies': toAdd}).json()
    print(x)
    y = requests.post(traktbaseurl + '/sync/watchlist/remove', headers=getTraktHeaders(), json={'movies': toRemove}).json()
    print(y)


def getTraktWatchlist():
    totale = []
    for type in ['movies']:
        x = requests.get(traktbaseurl + f'/sync/watchlist/{type}', headers=getTraktHeaders()).json()
        for item in x:
            if 'tmdb' not in item[type[:-1]]['ids']:
                continue
            totale.append(int(item[type[:-1]]['ids']['tmdb']))
    return totale


def getLbdWatchlist():
    headers = getLetterboxdHeader()
    cursor = 'start=0'
    totale = []
    while True:
        x = requests.get(letterboxdbaseurl + f'/member/{lbduid}/watchlist?perPage=100&cursor={cursor}', headers=headers).json()
        if 'items' not in x:
            return totale
        for item in x['items']:
            for link in item['links']:
                if link['type'] == 'tmdb':
                    if 'movie' in link['url']:
                        totale.append(int(link['id']))
                    break
        if 'next' not in x:
            return totale
        cursor = x['next']


if __name__ == '__main__':
    setWatchlist()
