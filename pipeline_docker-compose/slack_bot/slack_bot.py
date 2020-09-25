import slack
import os
import sqlalchemy
import time
import logging
logging.basicConfig(level=logging.DEBUG)


# oauth_token = SLACKBOT_TOKEN  # this is an environment variable on my local machine
# slack_token = os.environ["SLACK_API_TOKEN"]   solution to get the environ var
oauth_token = "xoxb-1263169162151-1381809494389-uBK8Rv1RQ2t9VS5Whj5Cmiot"
client = slack.WebClient(token=oauth_token)


# response = client.chat_postMessage(
#     channel="botchannel",
#     text="testing! :-)")


# Connect to the PostgreSQL container
# Declare postgres config
HOST = 'mypg'
USERNAME = 'postgres'
PORT = '5432'
DB = 'postgres'
PASSWORD = '1234'

# Create a postgres connection and assign it to 'engine' variable
engine = sqlalchemy.create_engine(
    f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}')

# Retrieve last tweet and sentiment using SQLAlchemy
# SELECT * FROM tweets ORDER BY id DESC LIMIT 1;
#tweet_to_bot = engine.select([tweets]).order_by(db.desc(tweets.columns.id).limit(1))


query = """SELECT text, sentiment_score 
            FROM tweets 
            ORDER BY id DESC
            LIMIT 1;"""

query_result = engine.execute(query)


def query_to_dict(ret):
    if ret is not None:
        return [{key: value for key, value in row.items()} for row in ret if row is not None]
    else:
        return [{}]


tweet_dict_list = query_to_dict(query_result)
tweet_dict = tweet_dict_list[0]

tweet_text = tweet_dict['text']
sen_score = tweet_dict['sentiment_score']


logging.warning(
    f'This will be written to Slack: New tweet has arrived: {tweet_text}. The sentiment score of the tweet is {sen_score}')

# post a message once an hour
while True:
    response = client.chat_postMessage(
        channel="botchannel",
        text=f"New tweet has arrived: \n\n{tweet_text}\n\n The sentiment score of the tweet is: \n{sen_score}")

    logging.warning('-- The tweet has been written to Slack Channel -----')
    time.sleep(3600)
