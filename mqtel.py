#!/home/cloud/miniconda3/envs/telegram/bin/python

import telegram
import paho.mqtt.client as mqtt
import os
import time
import json

## Get credentials from files
bot_auth = os.environ['HOME']+"/.credentials/bot.json"
mqtt_auth = os.environ['HOME']+"/.credentials/mqtt.json"
botdic = json.load(open(bot_auth, "r"))
mqttdic = json.load(open(mqtt_auth, "r"))
chatid = botdic["chatid"]

## MQTT callbacks
def on_connect(mqttc, obj, flags, rc):
    codedic = {
        0:"Connection successful",
        1:"Connection refused - incorrect protocol version",
        2:"Connection refused - invalid client identifier",
        3:"Connection refused - server unavailable",
        4:"Connection refused - bad username or password",
        5:"Connection refused - not authorised",
        6:"Response Code not defined",
        }
    if (rc>=0) and (rc<6):
        resp = codedic.get(rc)
    else:
        resp = codedic.get(6)
    print("MQTT broker connection Status: " + resp)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(time.asctime() + " : Unexpected disconnection.")

def on_message(mqttc, obj, msg):
    ## post bot message
    global mybot
    global chatid
    #mybot.sendMessage(chatid, str(msg.payload))
    print("[MQTT msg]: " + str(msg.payload))


## MQTT client settings
mqclient = mqtt.Client(client_id="mqtel")
mqclient.username_pw_set(mqttdic["username"], password=mqttdic["password"])
mqclient.on_connect = on_connect
mqclient.on_disconnect = on_disconnect
mqclient.on_message = on_message
mqclient.will_set('PINK/mqtel/status', payload="Not running", qos=0, retain=True)
mqclient.connect(mqttdic['URL'], port=mqttdic['PORT'], keepalive=60)

## Sub
mqclient.subscribe('PINK/mqtel/text')

## Start and test connection
mqclient.loop_start()
time.sleep(3)
if mqclient.is_connected():
    mqclient.publish("PINK/mqtel/status", "Connected", qos=0)
else:
    print("MQTT server not connected to broker. Abort.")
    sys.exit()

print("MQTT bridge server is running...")

while(1):
    time.sleep(1)

print("OK")
