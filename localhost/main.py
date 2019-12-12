import json
import requests
import sqlite3
import time
import random

PROXIES_LIST = [
    '51.158.98.121:8811',
    '51.158.68.133:8811',
    '51.158.68.68:8811',
    '163.172.147.94:8811',
    '51.158.68.26:8811',
    '51.158.99.51:8811',
    '51.158.123.35:8811',
    '163.172.152.52:8811',
    '51.158.108.135:8811',
    '51.75.161.44:3128',
]

random.shuffle(PROXIES_LIST)


def requests_get(url):
    for proxy in PROXIES_LIST:
        try:
            PROXIES = {
                'http': f'http://{proxy}',
                'https': f'https://{proxy}',
            }
            r = requests.get(url, proxies=PROXIES)
            if r.status_code == 200:
                return r.content
        except:
            pass


def timer():
    try:
        print('BEGIN parse ', time.asctime())
        api_url = 'https://2ch.hk'
        connect = sqlite3.connect('./main.db')
        content = requests_get(f'{api_url}/b/threads.json')
        for thread in json.loads(content)['threads']:
            print(thread["num"])
            content = requests_get(f'{api_url}/b/res/{thread["num"]}.json')
            for post in json.loads(content)['threads'][0]['posts']:
                if post['timestamp'] < (round(time.time()) - 300):
                    for file in post['files']:
                        # if file['size'] <= 7999:
                        if file['type'] == 10 or file['type'] == 6:
                            cursor = connect.cursor()
                            cursor.execute('SELECT * FROM `files` WHERE md5=?', (file['md5'],))
                            if not cursor.fetchone():
                                print(file['path'])
                                path = file['md5'] + '.' + file['path'].split('.').pop()
                                content = requests_get(f'{api_url}' + file['path'])
                                open('./files/' + path, 'wb').write(content)
                                thumbnail = file['md5'] + '.' + file['thumbnail'].split('.').pop()
                                content = requests_get(f'{api_url}' + file['thumbnail'])
                                open('./files/' + thumbnail, 'wb').write(content)
                                t = (file['md5'], thumbnail, path, file['fullname'], file['name'])
                                cursor.execute('INSERT INTO `files` VALUES (?, ?, ?, ?, ?)', t)
                                connect.commit()
        connect.close()
        print('END parse ', time.asctime())
    except Exception as e:
        print(e)
    timer()


if __name__ == "__main__":
    timer()
