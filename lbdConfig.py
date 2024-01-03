import requests
from datetime import datetime, timedelta
from mongoConfig import db
from config import *

letterboxdbaseurl = 'https://api.letterboxd.com/api/v0'
lbduid = LETTERBOXD_ID
client_id = LETTERBOXD_CLIENT
client_secret = LETTERBOXD_SECRET
username = LETTERBOXD_USERNAME
password = LETTERBOXD_PWD


def refreshToken():
    global tokenjson
    tokenjson = {}
    data = {'grant_type': 'refresh_token',
            'refresh_token ': tokenjson['refresh']}
    resp = requests.post(letterboxdbaseurl + '/auth/token', data=data).json()
    tokenjson = resp
    tokenjson['expire'] = datetime.now() + timedelta(seconds=resp['expires_in'])
    db.Tokens.update_one({'_id': 0}, {'$set': tokenjson}, upsert=True)


def requestToken():
    global tokenjson
    tokenjson = {}
    data = {'grant_type': 'password', 'client_id': client_id,
            'client_secret': client_secret,
            'username': username, 'password': password}
    resp = requests.post(letterboxdbaseurl + '/auth/token', data=data).json()
    tokenjson = resp
    tokenjson['expire'] = datetime.now() + timedelta(seconds=resp['expires_in'])
    tokenjson['name'] = 'letterboxd'
    db.Tokens.update_one({'_id': 0}, {'$set': tokenjson}, upsert=True)


def getToken():
    global tokenjson
    try:
        tokenjson
    except:
        tokenjson = db.Tokens.find_one({'_id': 0})
    try:
        if tokenjson['expire'] < datetime.now():
            if 'refresh_token' in tokenjson:
                refreshToken()
            else:
                requestToken()
    except:
        requestToken()
    return tokenjson['access_token']


def getLetterboxdHeader():
    return {"Authorization": "Bearer " + getToken()}


if __name__ == '__main__':
    print(getToken())
    print(getToken())
