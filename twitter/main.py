import twitter
import time
from credentials import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET
from color import COLOR, normalize
from mqtt import open_controller

api = twitter.Api(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token_key=ACCESS_TOKEN_KEY,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

keywords = ['分手', 'break-up', '別れる']


since_id = 0


def search(words):
    '找有某特關鍵字的 tweets'
    global since_id
    words = words[:8]
    term = '"{}"'.format('" OR "'.join(words))
    data = dict(
        term=term,
        result_type='recent'
    )
    if since_id:
        data['since_id'] = since_id
    statuses = api.GetSearch(**data)

    # 取得最後一筆的 id, 避免結果重覆
    ids = map(lambda status: status.id, statuses)
    since_id = max(ids, default=since_id)

    # 依關鍵字分類
    return list(

        (word, list(filter(lambda status: word in status.text, statuses)))
        for word in words
    )


def softer(color):
    return normalize(color, 25)

colors = [COLOR.RED, COLOR.GREEN, COLOR.BLUE, COLOR.YELLOW, COLOR.CYAN, COLOR.MAGENTA]
colors = list(map(softer, colors))


with open_controller(topic='pochang/iot/neopixel') as controller:
    leds = tuple(controller.leds())
    search(keywords)  # 拿掉第一筆結果, 因為沒意義
    while True:
        result = search(keywords)

        for index, ((word, statuses), led, color) in enumerate(zip(result, leds, colors)):
            if len(statuses):
                led.on(color)

            print('[{}]'.format(word))
            for status in statuses:
                print('\t', status.text[:70])  # 字數限制
        controller.flush()
        controller._reset()

        time.sleep(15)
        controller.flush()
        time.sleep(0)
        print('\n' * 5)
