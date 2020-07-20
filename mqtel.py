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

## tail setup
fpath = "/var/log/auth.log"

authlog = open(fpath, 'r')
dump = authlog.read()
del dump

print("Tailing file: " + fpath)
print("running ...")

try:
    while(1):
        newline = authlog.read()
        if len(newline)>3:
            if "cron:session" in newline:
                continue
            try:
                #print(newline, end="")
                bot.sendMessage(TL['chatid'], newline)
            except:
                print("failed to post message on TL")
        time.sleep(10)
except:
    pass

authlog.close()
print("OK")
