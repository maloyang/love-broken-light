import json
import requests_oauthlib
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


def twitter_search_status(data):
    '使用 twitter search api 找關鍵字, 並回傳找到的 tweets'
    response = twitter.get('https://api.twitter.com/1.1/search/tweets.json', params=data)
    return response.json()['statuses']


since_id = 0


def search(words):
    '''
        找有特定關鍵字的 tweets 並分類
        回傳結果
            [
                (word1, [status1, status2, status3, ....]),
                (word2, [status4, status5, status6, ....]),
            ]
    '''
    global since_id

    data = dict(
        q='"{}"'.format('" OR "'.join(words)),
        result_type='recent'
    )

    # 過澽掉舊的 tweets
    if since_id:
        data['since_id'] = since_id

    # 呼叫 twitter search api
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
    '改變亮度'
    return normalize(color, 5)


keywords = ['分手', 'broke up', '別れる', 'heartbroken']
colors = [COLOR.RED, COLOR.GREEN, COLOR.BLUE, COLOR.YELLOW]
colors = list(map(softer, colors))


with start_leds(topic='pochang/iot/neopixel') as leds:
    search(keywords)  # 拿掉第一筆結果, 因為都舊資料了

    # 開始每 15 秒更新一次
    while True:
        result = search(keywords[:8])  # 搜尋並限制關鍵字上限

        for (word, statuses), led, color in zip(result, leds, colors):
            if len(statuses):  # 如果有找到, 就設定亮燈
                led.on(color)

            print('[{}]'.format(word))
            for status in statuses:
                print('\t', status['text'][:70])  # 設定 print 的字數限制

        # 將結果更新到 LED 上
        leds.flush()
        leds._reset()

        time.sleep(15)
        leds.flush()
        time.sleep(0)
        print('\n' * 5)
