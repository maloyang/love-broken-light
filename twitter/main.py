import json
import requests_oauthlib
import urllib
import time
from credentials import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET
from color import COLOR, normalize
from mqtt import start_leds


twitter = requests_oauthlib.OAuth1Session(
    client_key=CONSUMER_KEY,
    client_secret=CONSUMER_SECRET,
    resource_owner_key=ACCESS_TOKEN_KEY,
    resource_owner_secret=ACCESS_TOKEN_SECRET,
)


since_id = 0


def twitter_search_status(data):
    qs = urllib.parse.urlencode(data)
    response = twitter.get('https://api.twitter.com/1.1/search/tweets.json?{}'.format(qs))
    return response.json()['statuses']


def search(words):
    '找有某特關鍵字的 tweets'
    global since_id
    words = words[:8]
    term = '"{}"'.format('" OR "'.join(words))
    data = dict(
        q=term,
        result_type='recent'
    )
    if since_id:
        data['since_id'] = since_id
    statuses = twitter_search_status(data)

    # 取得最後一筆的 id, 避免結果重覆
    ids = map(lambda status: status['id'], statuses)
    since_id = max(ids, default=since_id)

    # 依關鍵字分類
    return list(
        (word, list(filter(lambda status: word in status['text'], statuses)))
        for word in words
    )


def softer(color):
    return normalize(color, 5)


keywords = ['分手', 'break-up', '別れる', 'heartbroken']
colors = [COLOR.RED, COLOR.GREEN, COLOR.BLUE, COLOR.YELLOW]
colors = list(map(softer, colors))


with start_leds(topic='pochang/iot/neopixel') as leds:
    search(keywords)  # 拿掉第一筆結果, 因為沒意義
    while True:
        result = search(keywords)

        for index, ((word, statuses), led, color) in enumerate(zip(result, leds, colors)):
            if len(statuses):
                led.on(color)

            print('[{}]'.format(word))
            for status in statuses:
                print('\t', status['text'][:70])  # 字數限制
        leds.flush()
        leds._reset()

        time.sleep(15)
        leds.flush()
        time.sleep(0)
        print('\n' * 5)
