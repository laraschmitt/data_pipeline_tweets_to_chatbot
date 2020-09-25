"""
Python module that

1) Extracts data from MongoDB
- connect to the database
- query the data

2) Transform the data
- perform sentiment analysis on it

3) Loads the data into a postgres database
- connect to the database
- create table
"""


import time
import logging
from pymongo import MongoClient
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Connect to the MongoDB database
# Initialize a MongoClient class here and assign it to client variable,
# it will communicate with mongodb
client = MongoClient('mongodb:27017')

# Declare the database to use
mongo_db = client.tweet_db

# Declare the collection to use
tweet_collection = mongo_db.tweets

# Declare postgres config
HOST = 'mypg'
USERNAME = 'postgres'
PORT = '5432'
DB = 'postgres'
PASSWORD = '1234'

# Create a postgres connection and assign it to 'engine' variable
engine = create_engine(f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}')

# create table 'tweets' in the postgres database
CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS tweets
                    (id SERIAL,
                    name VARCHAR(50),
                    text VARCHAR(500),
                    sentiment_score NUMERIC);'''

engine.execute(CREATE_QUERY)

# instantiate Vader
s = SentimentIntensityAnalyzer()

# functions for each step of the ETL process:


def extract():
    """ Extracts tweets from the MongoDB database"""
    tweets = list(tweet_collection.find())
    # tweets is a list of tweets, where each item is a tweet (datatype dict/cursor)
    return tweets


def transform(tweets):
    """ Transforms tweets that were extracted from MongoDB

    Parameters:
    -------------
    tweets: List of tweets that were extracted from the MongoDB database. """

    for tweet in tweets:
        tweet['sentiment_score'] = s.polarity_scores(tweet['text'])['compound']
    return tweets  # updated tweets list


def load(tweets):
    """ Loads transformed tweeets into the Postgres database

    Parameters:
    ------------
    tweets: List of tweets that were extracted from the MongoDB database and transformed """

    insert_query = 'INSERT INTO tweets (name, text, sentiment_score) VALUES (%s, %s, %s);'
    for tweet in tweets:
        engine.execute(
            insert_query, (tweet['username'], tweet['text'], tweet['sentiment_score']))

    tweet_collection.remove({})


while True:
    time.sleep(10)
    extracted_tweets = extract()
    transformed_tweets = transform(extracted_tweets)
    load(transformed_tweets)
    logging.warning(
        '----- New list of tweets has been written into the Postgres database-----')
