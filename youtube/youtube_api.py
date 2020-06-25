from apiclient.discovery import build
import key
from tqdm import tqdm
from pprint import pprint
import re
import datetime
import csv


def main(q, num):
    youtube = build(
        'youtube',
        'v3',
        developerKey=key.API_KEY
    )

    dic_list = []

    search_res = youtube.search().list(
        part='snippet',
        q=q,
        order='viewCount',
        type='video'
    )

    DICT_CSV = {

    }

    data_list = []

    for _ in tqdm(range(num)):
        outputs = search_res.execute()

        for output in outputs['items']:
            snip = output['snippet']
            video_id = output['id']['videoId']

            datas = {
                'タイトル': snip['title'],
                'URL': f'https://www.youtube.com/watch?v={video_id}',
                'チャンネル名': snip['channelTitle'],
                'チャンネルURL': f'https://www.youtube.com/channel/{snip["channelId"]}',
                '再生時間': get_duration(video_id),
                '投稿日': snip['publishedAt'],
            }

            data_list.append(datas)

        search_res = youtube.search().list_next(search_res, outputs)

    dict_to_csv(data_list)


def dict_to_csv(dict_list: list):
    HEADER = [
        'タイトル',
        'URL',
        'チャンネル名',
        'チャンネルURL',
        '再生時間',
        '投稿日',
    ]
    with open('datas.csv', 'w') as f:
        writer = csv.DictWriter(f, HEADER)
        writer.writeheader()
        [writer.writerow(x) for x in dict_list]


def get_duration(id_):
    youtube = build(
        'youtube',
        'v3',
        developerKey=key.API_KEY
    )
    search_res = youtube.videos().list(
        part='statistics,contentDetails',
        id=id_,
    ).execute()

    duration = ConvertDuration(
        str(
            search_res['items'][0]['contentDetails']['duration']
        )
    )

    duration = str(datetime.timedelta(seconds=duration))

    return duration


def ConvertDuration(string):
    string = string.replace('PT', '')
    strings = re.split('\D', string)[:-1]
    if(len(strings) == 3):
        delta = datetime.timedelta(
            hours=int(strings[0]),
            minutes=int(strings[1]),
            seconds=int(strings[2])
        )
    elif(len(strings) == 2):
        delta = datetime.timedelta(
            minutes=int(strings[0]),
            seconds=int(strings[1])
        )
    elif(len(strings) == 1):
        delta = datetime.timedelta(
            seconds=int(strings[0])
        )
    else:
        delta = datetime.timedelta(
            seconds=0
        )

    return delta.seconds


if __name__ == '__main__':
    main('料理', 60)
