import twitter
import time
from credentials import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

api = twitter.Api(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token_key=ACCESS_TOKEN_KEY,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

keywords = ['分手', 'break-up']


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

    # extract max_id
    ids = map(lambda status: status.id, statuses)
    since_id = max(ids, default=since_id)
    return statuses

while True:
    statuses = search(keywords)
    for status in statuses:
        print(status.id, status.created_at, '\n', status.text)

    time.sleep(20)
    print('\n' * 5)
