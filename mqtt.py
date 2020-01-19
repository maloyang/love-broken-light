#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple
from contextlib import contextmanager
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
        '連線建立完成的動作'
        m = 'Connected flags' + str(flags) + ', result code ' + str(rc) + ', client_id  ' + str(client)
        print(m)

    def connect(self):
        '連線'
        self.client.connect(*self.broker)
        # 有自己的while loop，所以call loop_start()，不用loop_forever
        self.client.loop_start()
        time.sleep(2)
        print('loop start')

    def publish(self, topic, data):
        '送出'
        self.client.publish(topic, data)

    def disconnect(self):
        '離線'
        self.client.disconnect()


class LedController:
    def _reset(self):
        '重置狀態'
        self.lights = [[0, 0, 0]] * 8

    def open(self, topic):
        '連線'
        self.topic = topic
        self.client = Client()
        self.client.connect()

    def flush(self):
        '送出燈號狀態'
        neo_cmd = {'light': self.lights, 'delay': 0}
        neo_cmd = json.dumps(neo_cmd)
        print('cmd: ', neo_cmd)
        self.client.publish(self.topic, neo_cmd)

    def update(self, index, rgb):
        '更新一個 LED'
        assert isinstance(rgb, RGB)
        self.lights[index % 8] = rgb

    def close(self):
        '關掉 led 跟離線'
        self._reset()
        self.flush()
        self.client.disconnect()


@contextmanager
def LED(topic):
    '自動建立連線, 自動關閉'
    controller = LedController()
    controller.open(topic)
    try:
        yield controller
    finally:
        controller.close()


if __name__ == '__main__':
    with LED(topic='pochang/iot/neopixel') as leds:
        idx = 0
        while True:
            idx += 1
            leds._reset()
            v = 5
            for i in range(1, 5):
                leds.update(idx + i, RGB(v * i, 0, v * i))
            leds.flush()
            time.sleep(2)
