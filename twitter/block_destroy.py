import Twitter_API
import json
import time
from tqdm import tqdm
from multiprocessing import Pool


def get_ids():
    twitter = Twitter_API.api_proc()

    url = 'https://api.twitter.com/1.1/blocks/ids.json'
    res = twitter.get(url)
    id_dict = json.loads(res.text)
    ids = id_dict['ids']
    twitter.close()

    return ids


def destroy(screen_name):
    twitter = Twitter_API.api_proc()

    url = f'https://api.twitter.com/1.1/blocks/destroy.json'

    params = {'user_id': screen_name}
    twitter.post(url, params=params)

    twitter.close()


def count():
    for i in range(10):
        time.sleep(1)
        print(10 - i)


def main():
    ids = get_ids()
    if len(ids) == 0:
        exit()
    pool = Pool(processes=10)
    print('-' * 10)
    with tqdm(total=len(ids)) as t:
        for _ in pool.imap_unordered(destroy, ids):
            t.update(1)


if __name__ == "__main__":
    for i in range(99):
        main()
