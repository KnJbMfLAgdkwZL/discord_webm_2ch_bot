import discord
import json
import os
import requests
import sqlite3
import time

client = discord.Client()


@client.event
async def on_ready():
    async def timer():
        print('Logged in as: ', client.user.name, ' BEGIN parse ', time.asctime())
        PROXIES = {
            'http': 'http://163.172.189.32:8811',
            'https': 'https://163.172.189.32:8811',
        }
        api_url = 'https://2ch.hk'
        connect = sqlite3.connect('./main.db')
        r = requests.get(f'{api_url}/b/threads.json', proxies=PROXIES)
        for thread in json.loads(r.content)['threads']:
            r = requests.get(f'{api_url}/b/res/{thread["num"]}.json', proxies=PROXIES)
            for post in json.loads(r.content)['threads'][0]['posts']:
                if post['timestamp'] < (round(time.time()) - 300):
                    for file in post['files']:
                        if file['type'] == 10 or file['type'] == 6:
                            if file['size'] <= 7999:
                                cursor = connect.cursor()
                                cursor.execute('SELECT * FROM `files` WHERE md5=?', (file['md5'],))
                                if not cursor.fetchone():
                                    r = requests.get(f'{api_url}' + file['path'], proxies=PROXIES)
                                    name_save = './files/' + file['name']
                                    open(name_save, 'wb').write(r.content)
                                    channel = client.get_channel(653758320896770050)
                                    await channel.send(file=discord.File(name_save))
                                    t = (file['md5'], file['thumbnail'], file['path'], file['fullname'], file['name'])
                                    cursor.execute('INSERT INTO `files` VALUES (?, ?, ?, ?, ?)', t)
                                    connect.commit()
                                    os.remove(name_save)
        connect.close()
        print('END parse ' + time.asctime())
        await timer()

    await timer()


if __name__ == "__main__":
    client.run('1234567890', bot=False)
