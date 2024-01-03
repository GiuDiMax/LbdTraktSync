import requests
from datetime import datetime, timedelta
from mongoConfig import db
from config import *

traktbaseurl = 'https://api.trakt.tv'
client_id = TRAKT_CLIENT
client_secret = TRAKT_SECRET
code = TRAKT_CODE


def refreshToken():
    global tokenjson
    data = {'refresh_token': tokenjson['refresh_token'], 'client_id': client_id, 'client_secret': client_secret,
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob', 'grant_type': 'refresh_token'}
    resp = requests.post(traktbaseurl + '/oauth/token', data=data).json()
    if 'error' in resp:
        return requestToken
    tokenjson = resp
    tokenjson['expire'] = datetime.now() + timedelta(seconds=resp['expires_in'])
    db.Tokens.update_one({'_id': 1}, {'$set': tokenjson}, upsert=True)


def requestToken():
    global tokenjson
    data = {'code': code, 'client_id': client_id, 'client_secret': client_secret,
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob', 'grant_type': 'authorization_code'}
    resp = requests.post(traktbaseurl + '/oauth/token', data=data).json()
    tokenjson = resp
    tokenjson['expire'] = datetime.now() + timedelta(seconds=resp['expires_in'])
    tokenjson['name'] = 'trakt'
    db.Tokens.update_one({'_id': 1}, {'$set': tokenjson}, upsert=True)


def getTraktToken():
    global tokenjson
    try:
        tokenjson
    except:
        tokenjson = db.Tokens.find_one({'_id': 1})
    try:
        if tokenjson['expire'] < datetime.now():
            if 'refresh_token' in tokenjson:
                refreshToken()
            else:
                requestToken()
    except:
        requestToken()
    return tokenjson['access_token']


def getTraktHeaders():
    return {"Content-Type": "application/json",
               "Authorization": "Bearer " + getTraktToken(),
               "trakt-api-version": "2",
               "trakt-api-key": client_id}


if __name__ == '__main__':
    print(getTraktToken())
    refreshToken()
