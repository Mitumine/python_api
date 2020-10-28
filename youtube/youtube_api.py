from apiclient.discovery import build
import key
from tqdm import tqdm
from pprint import pprint
import re
import datetime
import csv
import os


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
            ch_id = snip["channelId"]
            datas = {
                'タイトル': snip['title'],
                'URL': f'https://www.youtube.com/watch?v={video_id}',
                'チャンネル名': snip['channelTitle'],
                'チャンネルURL': f'https://www.youtube.com/channel/{snip["channelId"]}',
                '再生時間': get_duration(video_id),
                '投稿日': snip['publishedAt'],
                '再生回数': get_video_statistics(video_id, youtube)['viewCount'],
                'チャンネル登録者数': get_ch_statistics(ch_id, youtube)['subscriberCount'],
            }

            datas['再生回数/登録者数'] = get_percent(
                int(datas['再生回数']),
                int(datas['チャンネル登録者数'])
            )

            data_list.append(datas)

        search_res = youtube.search().list_next(search_res, outputs)

    export_csv('test.csv', data_list)


def get_percent(int_1, int_2):
    if int_2 == 0:
        return '100%'
    return '{:.2%}'.format(int_1 / int_2)


def get_ch_statistics(id, youtube):
    statistics = youtube.channels().list(
        part='snippet,statistics',
        id=id,
    ).execute()['items'][0]['statistics']
    return statistics


def get_video_statistics(id, youtube):
    statistics = youtube.videos().list(
        part='statistics',
        id=id
    ).execute()['items'][0]['statistics']
    return statistics


def export_csv(file_name, rows):
    path = os.path.dirname(__file__)
    path += f'/{file_name}'

    keys = rows[0].keys()
    with open(path, 'w')as f:
        writer = csv.DictWriter(f, keys)
        header_row = {x: x for x in keys}
        writer.writerow(header_row)
        [writer.writerow(row) for row in rows]


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
    main('料理', 5)
