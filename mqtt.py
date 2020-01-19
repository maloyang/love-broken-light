#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple
import paho.mqtt.client as mqtt  # import the client1
import time
import random
import json


RGB = namedtuple('RGB', ['R', 'G', 'B'])


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


class LedController:
    def __init__(self, topic):
        self.topic = topic

    def _reset(self):
        '重置狀態'
        self.lights = [[0, 0, 0]] * 8

    def connect(self):
        '連線'
        self.client = Client()
        self.client.connect()

    def flush(self):
        '送出燈號狀態'
        neo_cmd = {'light': self.lights, 'delay': 0}
        neo_cmd = json.dumps(neo_cmd)
        print('cmd: ', neo_cmd)
        self.client.publish(self.topic, neo_cmd)

    def update(self, index, rgb):
        assert isinstance(rgb, RGB)
        self.lights[index % 8] = rgb


leds = LedController(topic='pochang/iot/neopixel')
leds.connect()

idx = 0
while True:
    idx += 1
    leds._reset()
    neo_light = [[0, 0, 0]] * 8
    v = 5
    for i in range(1, 5):
        leds.update(idx, RGB(v * i, 0, v * i))
    leds.flush()
    time.sleep(2)
