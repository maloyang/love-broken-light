#!/usr/bin/python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt  # import the client1
import time
import random
import json


def on_connect(client, userdata, flags, rc):
    m = "Connected flags" + str(flags) + ", result code " + str(rc) + ", client_id  " + str(client)
    print(m)

# some online free broker:
#   iot.eclipse.org
#   test.mosquitto.org
#   broker.hivemq.com
broker_address = "broker.hivemq.com"
TOPIC_BASE = 'pochang/iot'
topic_light = TOPIC_BASE + "/light"
topic_neopixel = TOPIC_BASE + "/neopixel"

client1 = mqtt.Client()  # create new instance
client1.on_connect = on_connect  # attach function to callback

time.sleep(1)
client1.connect(broker_address, 1883, 60)  # connect to broker

# client1.loop_forever()
# 有自己的while loop，所以call loop_start()，不用loop_forever
client1.loop_start()  # start the loop
time.sleep(2)
print("loop start")
idx = 0
while True:
    idx += 1

    neo_light = [[0, 0, 0]] * 8
    v = 5
    for i in range(1, 5):
        neo_light[(idx + i) % 8] = [v * i, 0, v * i]
    neo_cmd = {'light': neo_light, 'delay': 0}
    neo_cmd = json.dumps(neo_cmd)
    print('cmd: ', neo_cmd)
    client1.publish(topic_neopixel, neo_cmd)
    time.sleep(2)
