import json

import tweepy
from tweepy import OAuthHandler

credentials = json.load(open('credentials_tokens.json'))

consumer_key = credentials["consumer_key"]
consumer_secret = credentials["consumer_secret"]
access_token = credentials["access_token"]
access_secret = credentials["access_secret"]

# Authenticate with your app credentials
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
# search tweet's for keywords
with open('search.json', 'w') as f:
    for status in tweepy.Cursor(api.search, q="advanced analytics solutions").items(5):
        f.writelines(json.dumps(status._json, indent=4, sort_keys=True))
        print status.user.name
