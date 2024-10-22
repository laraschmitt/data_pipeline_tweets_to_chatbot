import credentials
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
import logging
from pymongo import MongoClient


def authenticate():
    """Function for handling Twitter Authentication. Please note
       that this script assumes you have a file called credentials.py
       which stores the 4 required authentication tokens:

       1. CONSUMER_API_KEY
       2. CONSUMER_API_SECRET
       3. ACCESS_TOKEN
       4. ACCESS_TOKEN_SECRET

    See course material for instructions on getting your own Twitter credentials.
    """
    auth = OAuthHandler(credentials.CONSUMER_API_KEY,
                        credentials.CONSUMER_API_SECRET)
    auth.set_access_token(credentials.ACCESS_TOKEN,
                          credentials.ACCESS_TOKEN_SECRET)

    return auth


# connect to MongoDB database:
client = MongoClient('mongodb:27017')
db = client.tweet_db


class TwitterListener(StreamListener):

    def on_data(self, data):
        """
        Gets called by Tweepy when a new tweet arrives.

        Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""

        t = json.loads(data)  # t is just a regular python dictionary.

        tweet = {
            'twitter_id': t['id'],
            'text': t['text'],
            'username': t['user']['screen_name'],
            'followers_count': t['user']['followers_count']
        }
        logging.warning('-----A new tweet has arrived ----------')
        print(t['text'] + '\n\n')

        # write a tweet to mongoDB
        db.tweets.insert_one(tweet)
        logging.warning('-- The tweet has been inserted into MongoDB -----')

        #logging.critical(f'\n\n\nTWEET INCOMING: {tweet["text"]}\n\n\n')

    def on_error(self, status):
        print("error: ", status,
              "means: app is being rate limited for making too many requests")
        if status == 420:
            print(status)
            return False

#


if __name__ == '__main__':

    auth = authenticate()  # log into twitter
    # print(auth.get_username())
    listener = TwitterListener()  # create a listener
    # starts an infinite loop  that listens to Twitter
    stream = Stream(auth, listener)  # Data Stream --> infinite flow of data
    stream.filter(track=['ultralight hiking',
                         'ultralight packing', 'ultralight', 'hiking'], languages=['en'])
