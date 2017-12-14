# !!! Note that the search results at twitter.com may return historical results while the Search API usually only serves tweets from the PAST WEEK !!! https://dev.twitter.com/rest/public/search
# With "GET statuses/user_timeline" (https://dev.twitter.com/rest/reference/get/statuses/user_timeline) you can get up to 3200 latest tweets, but this is awful as well.
# If you need a way to get old tweets, you can get them from individual users (may be not allowed, robots.txt) because collecting tweets from them is limited by number rather than time (so in many cases you can go back months or years).
# TO AVOID THESE RESTRICTIONS TRY THE FOLLOWING SCRIPT.
# Or with Python3 try this (not tested): https://github.com/bpb27/twitter_scraping/
# Andreas

import pandas, time, sys
import numpy as np
import json
# Python 2.7 required. For Python 3 download "got3" from here https://github.com/Jefferson-Henrique/GetOldTweets-python and adjust.
import got  # Actually explained here: https://github.com/Jefferson-Henrique/GetOldTweets-python/issues/52 , but to sum up:

# First pip install lxml==3.5.0 & pip install pyquery==1.2.10, then download the "got"-folder (also on Confluence) and copy it into you site packages folder;

RESULTSFILE = 'tweeted_'  # Some name for the csv-file with exported results
MAXTWEETS = 50  # Set the max number of tweets to receive from crawling for each name/SME.

# load SMEs' names (or some other names to search twitter for):
sme = pandas.read_csv('twt.csv', sep='|', header=0, encoding='utf-8')  # Opel SME customers
tweets = pandas.Series()

f = open("tweeeet.json", "a")
# Get the tweets:
for name in sme['keywords']:
    tw = u''
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(name).setSince("2017-01-01").setUntil(
        "2017-12-11").setMaxTweets(MAXTWEETS)
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    for i in tweet:
        tw = tw +"\n"+ i.username
    tweets = tweets.append(pandas.Series([tw]))
sme = sme.assign(tweets=tweets.values)

f.close()
# For testing:
forNaNcounting = pandas.Series()
for twt in sme['tweets']:
    if twt == '':
        forNaNcounting = forNaNcounting.append(pandas.Series([np.nan]))
    else:
        forNaNcounting = forNaNcounting.append(pandas.Series([twt]))
print 'Percentage found/all: ' + str(100 * (len(sme.index) - forNaNcounting.isnull().sum()) / len(sme.index))

# Export into csv:
actual = str(time.strftime("%d %b %Y %H %M %S"))  # Just to keep track...
RESULTSFILE = RESULTSFILE + actual[:11] + 'TIME' + actual[11:]  # Just to keep track...
pth =   RESULTSFILE + '.csv'
open(pth, 'a').close()  # Create the file to store/export.
sme.to_csv(path_or_buf=pth, sep='|', encoding='utf-8')  # Export.
