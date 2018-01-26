import urllib
from git import Repo
import os.path
import json
import time



dir=os.path.dirname(os.path.abspath(__file__))+'/'


if not os.path.isfile(dir+'/config.json'):
    f=open(dir+'/config.json','w+')
    f.write("""{
        "token":"xoxp-201177670631-199718697040-303091550880-410766a043392b9f558889dfb13961f7",
        "icon_url":"https://git-scm.com/images/logos/downloads/Git-Icon-1788C.png",
        "user":"Git",
        "repo":{
            "Crypto":{
                "path":"../exchange/",
                "channels":[
                    "C8XPS6868"
                ]
            }
        }
    }""")
    f.close()
    print "Setup your config.json"
    exit()
try:
    with open(dir+'/config.json') as f:
        config= f.read()
        config=json.loads(config)
except Exception as e:
    print('--------------------------Invalid config--------------------------')
    print(e)
    exit()
def send(message,channel):
    global config
    data={
        'token': config['token'],
        'channel': channel,
        'text': message,
        'icon_url': config['icon_url'],
        'username': config['user'],
    }
    response = urllib.urlopen('https://slack.com/api/chat.postMessage?'+urllib.urlencode(data, True))
    html = response.read()
    html=json.loads(html)
    return html

for name in config['repo']:
    config['repo'][name]['commits']=[]
    for channel in config['repo'][name]['channels']:
        # print send('Connected to git repository '+name,channel)['ok']
        if not send('Connected to git repository '+name,channel)['ok']:
            print name+' Invalid channel '+channel

while True:
    for name in config['repo']:
        config['repo'][name]['repo'] = Repo(config['repo'][name]['path'])
        for remote in config['repo'][name]['repo'].remotes:
            remote.fetch()
        loginfo = config['repo'][name]['repo'].git.log('--branches','--remotes', '--pretty=format=%h%x09%an%x09%s')
        loginfo=loginfo.replace('format=','').split("\n")
        l=loginfo[0].split("\t")
        if len(config['repo'][name]['commits'])==0:
            config['repo'][name]['commits'].append(l)
            print(config['repo'][name]['commits'])
        elif config['repo'][name]['commits'][len(config['repo'][name]['commits'])-1][0]!=l[0]:
            config['repo'][name]['commits'].append(l)
            print(config['repo'][name]['commits'])
            for channel in config['repo'][name]['channels']:
                send(name+": "+l[1]+' '+l[2],channel)
    time.sleep(1)
