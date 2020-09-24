import slackclient
import pyjokes

oauth_token = SLACKBOT_TOKEN  # this is an environment variable on my local machine

client = slack.WebClient(token=oauth_token)
joke = pyjokes.get_joke()

response = client.chat_postMessage(
    channel='#random', text=f"Here is a Python joke: {joke}")
