import json
import time
from datetime import datetime

# Python 2.7 required. For Python 3 download "got3" from here https://github.com/Jefferson-Henrique/GetOldTweets-python and adjust.
# First pip install lxml==3.5.0 & pip install pyquery==1.2.10, then download the "got"-folder (also on Confluence) and copy it into you site packages folder;
import got
import pandas

try:
    settings = json.load(open('settings.json'))
    keywords = pandas.read_csv('keywords.csv')
except Exception, e:
    print 'Problem with settings.json or keywords.csv files: ' + str(e)
    print 'Aborting search...'
    exit(-1)

config = settings['old_tweet_configuration']

MAX_TWEETS = config['max_tweets'] or 100  # Set the max number of tweets to receive from crawling for each name.
TOP_TWEETS = config['top_tweets'] or False  # True for top tweet's

# By default search for 5 months old tweet's from today.
SINCE = config['since'] or datetime.fromtimestamp((time.time() - (60 * 60 * 24 * 30 * 5))).strftime("%Y-%m-%d")
UNTIL = config['until'] or datetime.now().strftime("%Y-%m-%d")

print 'Crawling tweet\'s from {0} to {1}'.format(SINCE, UNTIL)

profile_link_prefix = 'https://twitter.com/'
leads = {'Name': [], 'Handle': [], 'Profile_Link': []}

# Get the tweets:
for key, tag in zip(keywords['Keywords'], keywords['HashTags']):
    tw = u''
    query = key.strip() + ' OR ' + tag.strip()
    tweetCriteria = got.manager.TweetCriteria() \
        .setQuerySearch(query) \
        .setSince(since=SINCE) \
        .setUntil(until=UNTIL) \
        .setMaxTweets(maxTweets=MAX_TWEETS) \
        .setTopTweets(topTweets=TOP_TWEETS)

    search_count = 0
    print("searching for: " + query)
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)

    for i in tweet:
        username = '@' + (str(i.username)[2:])
        leads['Name'].append(i.fullName)
        leads['Handle'].append(username)
        leads['Profile_Link'].append(profile_link_prefix + username[1:])
        search_count += 1
    print('Found {} matching tweets.'.format(search_count))

search_leads = pandas.DataFrame.from_dict(leads)

search_leads.drop_duplicates(subset=['Handle'], keep=False, inplace=True)
search_leads.reset_index(drop=True, inplace=True)

try:
    filter_handles = pandas.read_csv('filter.csv')
    search_leads = search_leads[~search_leads.Handle.isin(filter_handles.Handle)]
except:
    print 'No filter csv found!'

print 'Total {} tweets found'.format(len(leads['Handle']))
print '{} unique twitter handles.'.format(search_leads.shape[0])

search_leads.to_csv(path_or_buf='old_tweets.csv', sep=',', encoding='utf-8', index=False)
