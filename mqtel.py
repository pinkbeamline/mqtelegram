#!/home/cloud/miniconda3/envs/telegram/bin/python

import telegram
import os
import json
import time

## Get credentials
TLpath = os.environ['HOME']+"/.credentials/bot.json"
TL = json.load(open(TLpath, "r"))

## bot setup
bot = telegram.Bot(TL['token'])

## file setup
fpath = "/var/log/auth.log"
fsizelast = os.stat(fpath).st_size 

authlog = open(fpath, 'r')
dump = authlog.read()
del dump

## date setup
print("Tailing file: " + fpath)
print("running ...")

try:
    while(1):
        fsizenow = os.stat(fpath).st_size
        if os.stat(fpath).st_size < fsizelast:
            fsizelast = fsizenow
            authlog.close()
            authlog = open(fpath, 'r')
            dump = authlog.read()
            del dump

        newline = authlog.read()
        if len(newline)>3:
            if "cron:session" in newline:
                continue
            try:
                print(newline)
                bot.sendMessage(TL['chatid'], newline)
            except:
                print("failed to post message on TL")
        time.sleep(10)
except:
    pass

authlog.close()
print("OK")
