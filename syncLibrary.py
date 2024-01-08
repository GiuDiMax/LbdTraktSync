from lbdConfig import getLetterboxdHeader, letterboxdbaseurl, lbduid, listid
import requests
from traktConfig import getTraktHeaders, traktbaseurl


def getDiff():
    a = getTraktLibrary()
    b = getLetterboxdLibrary()
    mancanti = []
    toRemove = []
    movies = []
    print("ok req")
    for film in b:
        check = False
        for film2 in a:
            if int(film['tmdb']) == int(film2['tmdb']):
                check = True
                if film['notes'] != film2['notes']:
                    mancanti.append(film2)
                break
        if not check:
            toRemove.append(film['id'])
    for film in a:
        check = False
        for film2 in b:
            if int(film['tmdb']) == int(film2['tmdb']):
                check = True
                break
        if not check:
            mancanti.append(film)
    z = 0
    print(len(mancanti))
    print("to remove")
    print(toRemove)
    for x in mancanti:
        z = z + 1
        idx = getLbd(x['tmdb'])
        if idx is None:
            continue
        if x['notes'] != '':
            movies.append({'film': idx, 'notes': x['notes']})
        else:
            movies.append({'film': idx})
        if z >= 50:
            addMovies(toRemove, movies)
            movies = []
            toRemove = []
            z = 0
    addMovies(toRemove, movies)


def getTraktLibrary():
    totale = []
    for type in ['movies']:
    #for type in ['movies', 'shows']:
        if type == 'movies':
            meta = '?extended=metadata'
        else:
            meta = ""
        x = requests.get(traktbaseurl + f'/sync/collection/{type}{meta}', headers=getTraktHeaders()).json()
        for item in x:
            if 'tmdb' not in item[type[:-1]]['ids']:
                continue
            note = ""
            if 'metadata' in item:
                if item['metadata']['resolution']:
                    note = note + item['metadata']['resolution']
                if item['metadata']['hdr']:
                    note = note + ' HDR'
                if item['metadata']['audio']:
                    note = note + " " + item['metadata']['audio']
                if item['metadata']['audio_channels']:
                    note = note + " " + item['metadata']['audio_channels']
            totale.append({'tmdb': item[type[:-1]]['ids']['tmdb'], 'notes': note.replace("_", " ").upper()})
    return totale


def getLbd(tmdb):
    headers = getLetterboxdHeader()
    x = requests.get(letterboxdbaseurl + f'/films?filmId=tmdb:{tmdb}', headers=headers).json()['items']
    if len(x) > 0:
        return x[0]['id']
    else:
        return None


def addMovies(toRemove, movies):
    headers = getLetterboxdHeader()
    #headers['X-HTTP-Method-Override'] = 'PATCH'
    #674324
    #data = {'description': 'test2'}
    #data = {'entries': [{'film': fid, 'notes': 'test'}, {'film': fid2, 'notes': 'test'}], 'filmsToRemove': []}
    data = None
    if movies != []:
        data = {'entries': movies, 'filmsToRemove': toRemove}
    elif toRemove != []:
        data = {'filmsToRemove': toRemove}
    if data is None:
        return
    x = requests.patch(letterboxdbaseurl + f'/list/{listid}', headers=headers, json=data).json()
    if 'data' in x:
        print("ok")
    else:
        print("notok")


def getLetterboxdLibrary():
    headers = getLetterboxdHeader()
    cursor = 'start=0'
    totale = []
    while True:
        x = requests.get(letterboxdbaseurl + f'/list/{listid}/entries?cursor={cursor}', headers=headers).json()
        if 'items' not in x:
            print(x)
            return totale
        for item in x['items']:
            f = {}
            for link in item['film']['links']:
                if link['type'] == 'tmdb':
                    f['tmdb'] = link['id']
                    break
            if 'notesLbml' in item:
                f['notes'] = item['notesLbml']
            else:
                f['notes'] = ""
            f['id'] = item['film']['id']
            totale.append(f)
        if 'next' not in x:
            return totale
        cursor = x['next']


if __name__ == '__main__':
    #print(getLbd(84958))
    #print(getLetterboxdLibrary())
    getDiff()
