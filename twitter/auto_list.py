from Twitter_API import api_proc
import json


def main():

    TWITTER = api_proc()
    URL = 'https://api.twitter.com/1.1/friends/ids.json'
    PARAMS = {
        'screen_name': '_sotono',
    }

    req = TWITTER.get(URL, params=PARAMS)
    if req.status_code != 200:
        exit

    text = json.loads(req.text)
    ids = text['ids']

    for user_id in ids:
        URL = 'https://api.twitter.com/1.1/lists/members/create.json'
        PARAMS = {
            'list_id': 1276017567761494017,
            'user_id': user_id
        }
        req = TWITTER.post(URL, params=PARAMS)


if __name__ == "__main__":
    main()
