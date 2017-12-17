# !!! Note that the search results at twitter.com may return historical results while the Search API usually only serves tweets from the PAST WEEK !!! https://dev.twitter.com/rest/public/search
# With "GET statuses/user_timeline" (https://dev.twitter.com/rest/reference/get/statuses/user_timeline) you can get up to 3200 latest tweets, but this is awful as well.
# If you need a way to get old tweets, you can get them from individual users (may be not allowed, robots.txt) because collecting tweets from them is limited by number rather than time (so in many cases you can go back months or years).
# TO AVOID THESE RESTRICTIONS TRY THE FOLLOWING SCRIPT.
# Or with Python3 try this (not tested): https://github.com/bpb27/twitter_scraping/
# Andreas

import datetime
import json
import time

# Python 2.7 required. For Python 3 download "got3" from here https://github.com/Jefferson-Henrique/GetOldTweets-python and adjust.
import \
    got  # Actually explained here: https://github.com/Jefferson-Henrique/GetOldTweets-python/issues/52 , but to sum up:
import pandas

# First pip install lxml==3.5.0 & pip install pyquery==1.2.10, then download the "got"-folder (also on Confluence) and copy it into you site packages folder;

# load SMEs' names (or some other names to search twitter for):
settings = json.load(open('settings.json'))
keywords = pandas.read_csv('keywords.csv')

config = settings['old_tweet_configuration']
tweets = pandas.Series()
MAX_TWEETS = config['max_tweets']  # Set the max number of tweets to receive from crawling for each name/SME.
SINCE = config['since'] if config['since'] else datetime.datetime.fromtimestamp((time.time() - 2592000)).strftime(
    "%Y-%m-%d")
UNTIL = config['until'] if config['until'] else datetime.datetime.now().strftime("%Y-%m-%d")
TOP_TWEETS = config['top_tweets']

profile_link_prefix = 'https://twitter.com/'

columns = ['Name', 'Handle', 'Profile_Link']
search_leads = pandas.DataFrame([], [], columns)

lead_names = []
lead_handles = []
lead_profile_links = []

# Get the tweets:
for query in keywords['Keywords'].append(keywords['HashTags']).head():
    tw = u''
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query) \
        .setSince(since=SINCE) \
        .setUntil(until=UNTIL) \
        .setMaxTweets(maxTweets=MAX_TWEETS) \
        .setTopTweets(topTweets=TOP_TWEETS)

    search_count = 0
    print("searching for: " + query)
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)

    for i in tweet:
        lead_names.append(i.fullName)
        lead_handles.append('@' + (str(i.username)[2:]))
        search_count += 1
    search_leads['Name'] = pandas.Series(lead_names)
    search_leads['Handle'] = pandas.Series(lead_handles)
    search_leads['Profile_Link'] = profile_link_prefix + search_leads['Handle'].map(lambda x: str(x)[1:])
    print('Found {0} matching tweets.'.format(search_count))

search_leads.drop_duplicates(subset=['Handle'], keep=False, inplace=True)
search_leads.reset_index(drop=True, inplace=True)

search_leads.to_csv(path_or_buf='old_tweets.csv', sep=',', encoding='utf-8')
