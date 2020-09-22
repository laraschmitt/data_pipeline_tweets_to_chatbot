
### 🐳 Data pipeline using docker containers

Small project to analyze the sentiment of tweets using a dockerized data pipeline including 5 containers:

| <p style="font-size: 10px">container name</p>      | <p style="font-size: 10px">description</p>      | <p style="font-size: 10px">image</p> 
| ----------- | ----------- |  ----------- | 
| <p style="font-size: 10px">tweet_collector</p>      | <p style="font-size: 10px">collects tweets via the Twitter API and stores them in MongoDB</p>       | <p style="font-size: 10px">created</p>    
| <p style="font-size: 10px">mongodb</p>      | <p style="font-size: 10px">stores tweets as JSON documents</p>       | <p style="font-size: 10px">mongo</p>    
| <p style="font-size: 10px">ETL_job</p>      | <p style="font-size: 10px">analyzes sentiments of tweets and stores them in Postgres DB</p>       | <p style="font-size: 10px">created</p>    
| <p style="font-size: 10px">postgresdb</p>      | <p style="font-size: 10px">stores tweets and respective annotations in a table</p>       | <p style="font-size: 10px">postgres</p>
| <p style="font-size: 10px">slack_bot</p>      | <p style="font-size: 10px">published high rank tweets in a Slack channel</p>       | <p style="font-size: 10px">created</p>

This repo includes:
* skeleton pipeline
* python script to collect tweets via the twitter API and the `tweepy` module and store tweets in a Mongo DB
* create an ETL task
* sentiment analysis using the `Vader` module
  * read tweets from MongoDB
  * function to calculate the sentiment of a tweet
  * write the tweet (message & timestamp) and its sentiment to a postgresDB
* build slack bot

