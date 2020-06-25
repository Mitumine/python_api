import Twitter_API
import json
from tqdm import tqdm
from multiprocessing import Pool


def search_and_get_user(q: str, max_id=''):
    twitter = Twitter_API.api_proc()
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    params = {
        'q': q,
        'count': 100,
        'result_type': 'mixed',
        'max_id': max_id,
    }
    # 辞書整理
    if params['max_id'] == '':
        del params['max_id']

    req = twitter.get(url, params=params)
    req_dict = json.loads(req.text)

    # ユーザー一覧習得
    users = [
        user_id['user']['screen_name']
        for user_id
        in req_dict['statuses']
    ]

    # 次はここからはじまるよ
    next_id = req_dict['statuses'][-1]['id']

    twitter.close()
    return users, next_id


def get_userids(keyword: str):
    users_store = []
    next_id = ''
    print('-' * 10)
    print('Get User Name')
    for _ in tqdm(range(15)):
        users, next_id = search_and_get_user(keyword, next_id)
        users_store += users
        Twitter_API.get_rate_limit_status()
    users_store = list(set(users_store))
    return users_store


def destroy(screen_name):
    twitter = Twitter_API.api_proc()

    url = f'https://api.twitter.com/1.1/blocks/create.json'

    params = {'screen_name': screen_name}
    twitter.get(url, params=params)

    twitter.close()


def main(word: str):
    if word == '':
        return

    users = get_userids(word)
    pool = Pool(processes=10)

    print('-' * 10)
    print('Blocking')
    with tqdm(total=len(users)) as t:
        for _ in pool.imap_unordered(destroy, users):
            t.update(1)


if __name__ == "__main__":
    word = input('ブロックするワードを入力\n>>>> ')
    main(word)
