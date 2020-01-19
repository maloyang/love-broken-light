#!/usr/bin/python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt  # import the client1
import time
import random
import json


class Client:
    broker = ('broker.hivemq.com', 1883, 60)

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        m = 'Connected flags' + str(flags) + ', result code ' + str(rc) + ', client_id  ' + str(client)
        print(m)

    def connect(self):
        self.client.connect(*self.broker)
        # 有自己的while loop，所以call loop_start()，不用loop_forever
        self.client.loop_start()
        time.sleep(2)
        print('loop start')

    def publish(self, topic, data):
        self.client.publish(topic, data)

TOPIC_BASE = 'pochang/iot'
topic_light = TOPIC_BASE + '/light'
topic_neopixel = TOPIC_BASE + '/neopixel'

client = Client()
client.connect()

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
    client.publish(topic_neopixel, neo_cmd)
    time.sleep(2)
