import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

consumer_key = "ERaD9fEP8ARELnwfV5qbpbMYo" # The application's consumer key
consumer_secret = "vlG9htHUwmdMq3s271QUzgqrvTxnlXzFkBeNHMfWYMJYdaKVxr" # The application's consumer secret
access_token = "171383939-OOIv348clmL6mDDvNBEhcpRxYdsnO8wUEygbMleS" #The access token granted after OAuth authorization
access_secret = "xx5Of6kIDXytsH8PTqmIO6uwYIQLzFuBAo4MtzeRnkFXn" # The access token secret granted after OAuth authorization

## Authenticate with your app credentials
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# api = tweepy.API(auth)

## get tweet's from your timeline
# for status in tweepy.Cursor(api.home_timeline).items(5):
#     print status.text

class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True

        except BaseException as e:
            print "Error " + str(e)

        return True

    def on_error(self, status_code):
        print status_code
        return True

twitter_stream = tweepy.Stream(auth, MyListener())
twitter_stream.filter(track=['#WingsTourFinalDay3', '#HumanRightsDay'])
