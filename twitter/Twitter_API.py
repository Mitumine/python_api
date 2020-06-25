# -*- coding:utf8 -*-
from requests_oauthlib import OAuth1Session
import json
from time import sleep

import key

API_KEY = key.API_KEY
API_SECRET = key.API_SECRET
ACCESS_TOKEN = key.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = key.ACCESS_TOKEN_SECRET


def api_proc():
    # TwiterのAPIを使えるようにする
    api = OAuth1Session(
        API_KEY,
        API_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
    )

    return api


def get_rate_limit_status():
    Twitter = api_proc()
    limit = 1
    remaining = 1

    URL = "https://api.twitter.com/1.1/application/rate_limit_status.json"

    req = Twitter.get(URL)
    if req.status_code == 200:
        limit_api = json.loads(req.text)
        resources = limit_api['resources']['search']['/search/tweets']
        limit = resources['limit']
        remaining = resources['remaining']
        reset = resources['reset']
    else:
        print('-' * 30)
        print('Limit Twitter API !!')
        sleep(15*60)

    Twitter.close()

    return remaining


def test():
    pass


if __name__ == '__main__':
    pass
    test()
