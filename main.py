import json
import os
import requests
import sqlite3


class api_2ch:
    def __init__(self):
        self.files_dir = './files/'
        self.db = './main.db'
        self.url = 'https://2ch.hk/'
        self.proxies = {
            'http': 'http://51.75.164.92:3128',
            'https': 'https://51.75.164.92:3128',
        }

    def Get(self, url):
        return requests.get(url, proxies=self.proxies)

    def GetThreads(self, board):
        url = f'{self.url}{board}/threads.json'
        r = self.Get(url)
        return json.loads(r.content)

    def GetThread(self, board, thread):
        url = f'{self.url}{board}/res/{thread}.json'
        r = self.Get(url)
        return json.loads(r.content)

    def GetWbm(self, board):
        threads = self.GetThreads(board)
        for t in threads['threads']:
            thread = self.GetThread(board, t['num'])
            posts = thread['threads'][0]['posts']
            for p in posts:
                for f in p['files']:
                    if f['type'] == 10 or f['type'] == 6:
                        self.CheckFile(f)

    def CheckFile(self, f):
        connect = sqlite3.connect(self.db)
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM `files` WHERE md5=?', (f['md5'],))
        res = cursor.fetchone()
        if not res:
            self.Get_SaveFile(f['path'])
            self.Get_SaveFile(f['thumbnail'])
            t = (f['md5'], f['thumbnail'], f['path'], f['fullname'], f['name'])
            cursor.execute('INSERT INTO `files` VALUES (?, ?, ?, ?, ?)', t)
            connect.commit()
            print(f['path'])
        else:
            print('exist')
        connect.close()

    def Get_SaveFile(self, file):
        arr = file.split('/')
        arr = arr[:-1]
        dir = self.files_dir + "/".join(arr)
        if not os.path.exists(dir):
            os.makedirs(dir)
        url = self.url + file
        r = self.Get(url)
        open(self.files_dir + file, 'wb').write(r.content)


if __name__ == "__main__":
    api = api_2ch()
    api.GetWbm('b')
