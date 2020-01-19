import twitter
import time
from credentials import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET
from color import COLOR
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
    global since_id
    print('since', [since_id])
    words = words[:8]
    term = '"{}"'.format('" OR "'.join(words))
    data = dict(
        term=term,
        result_type='recent'
    )
    if since_id:
        data['since_id'] = since_id
    statuses = api.GetSearch(**data)

    # 取得最後一筆的 id
    ids = map(lambda status: status.id, statuses)
    since_id = max(ids, default=since_id)

    # 依關鍵字分類
    return list(

        (word, list(filter(lambda status: word in status.text, statuses)))
        for word in words
    )


with open_controller(topic='pochang/iot/neopixel') as controller:
    colors = [COLOR.RED, COLOR.GREEN, COLOR.BLUE, COLOR.YELLOW, COLOR.CYAN, COLOR.MAGENTA]
    leds = tuple(controller.leds())
    search(keywords)  # 拿掉第一筆結果, 因為沒意義
    while True:
        result = search(keywords)

        for index, ((word, statuses), led, color) in enumerate(zip(result, leds, colors)):
            if len(statuses):
                led.on(color)

            print('[{}]'.format(word))
            for status in statuses:
                print('\t', status.text)
        controller.flush()
        controller._reset()

        time.sleep(20)
        print('\n' * 5)
