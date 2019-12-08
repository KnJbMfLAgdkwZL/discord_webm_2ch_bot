import requests
import json


class api_2ch:
    def __init__(self):
        self.url = 'https://2ch.hk/'
        self.proxies = {
            'http': 'http://51.75.164.92:3128',
            'https': 'https://51.75.164.92:3128',
        }

    def GetThreads(self, board):
        url = f'{self.url}{board}/threads.json'
        r = requests.get(url, proxies=self.proxies)
        return json.loads(r.content)

    def GetThread(self, board, thread):
        url = f'{self.url}{board}/res/{thread}.json'
        r = requests.get(url, proxies=self.proxies)
        return json.loads(r.content)

    def GetWbm(self, board):
        threads = self.GetThreads(board)
        for t in threads['threads']:
            thread = self.GetThread(board, t['num'])
            posts = thread['threads'][0]['posts']
            for p in posts:
                for f in p['files']:
                    if f['type'] == 10 or f['type'] == 6:
                        str = ''
                        str += f['md5']
                        str += '\n'
                        str += f['thumbnail']
                        str += '\n'
                        str += f['path']
                        str += '\n'
                        str += f['fullname']
                        str += '\n'
                        str += f['name']
                        str += '\n'
                        print(str)
                        return


api = api_2ch()
api.GetWbm('b')
