import json

import pandas as pd
import tweepy

settings = json.load(open('credentials_tokens.json'))
keywords = pd.read_csv('keywords.csv')
profile_link_prefix = 'https://twitter.com/'

columns = ['Name', 'Handle', 'Verified', 'Bio', 'Profile_Link']
search_leads = pd.DataFrame([], [], columns)

lead_names = []
lead_handles = []
lead_bio = []
lead_verified = []

credentials = settings['credentials']
config = settings['search_configuration']

API_KEY = credentials["consumer_key"]
API_SECRET = credentials["consumer_secret"]
ACCESS_TOKEN = credentials['access_token']
ACCESS_SECRET = credentials['access_secret']

tweet_per_query = config["tweets_per_query"]

# Authenticate with your app credentials
auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if not api:
    print("Can't Authenticate, please check credentials.")
    exit(-1)


def parse_search_configuration(config):
    if config['country'] or config['city']:
        outh = tweepy.OAuthHandler(API_KEY, API_SECRET)
        outh.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(outh)

        query = config['country'] if config['country'] else config['city']
        granularity = 'country' if config['country'] else 'city'
        places = api.geo_search(query=query, granularity=granularity)

        if len(places) <= 0:
            print("City or Country you entered doesn't exist!")
            exit(-1)
        else:
            return places[0].id


print(parse_search_configuration(config))


# search tweet's for keywords
def search_twitter_for(search_keyword):
    search_count = 0
    print("searching for: " + search_keyword)
    with open('search.json', 'w') as f:
        for status in tweepy.Cursor(api.search, q=search_keyword,
                                    count=tweet_per_query,
                                    since_id=None).items():
            tweet_json = status._json
            f.writelines(json.dumps(tweet_json, indent=4, sort_keys=True))
            lead_names.append(tweet_json['user']['name'])
            lead_handles.append(tweet_json['user']['screen_name'])
            lead_bio.append(tweet_json['user']['description'])
            lead_verified.append(tweet_json['user']['verified'])
            search_count += 1
            print(tweet_json['user']['name'])
        search_leads['Name'] = pd.Series(lead_names)
        search_leads['Handle'] = pd.Series(lead_handles)
        search_leads['Verified'] = pd.Series(lead_verified)
        search_leads['Bio'] = pd.Series(lead_bio)
        search_leads['Profile_Link'] = profile_link_prefix + search_leads['Handle']
        print('Found {0} matching tweets.'.format(search_count))


# for key in keywords['Keywords'].append(keywords['HashTags']):
search_twitter_for(keywords['Keywords'][2])
#
search_leads.drop_duplicates(subset=['Handle'], keep=False, inplace=True)
search_leads.reset_index(drop=True,inplace=True)
#
search_leads.to_csv(path_or_buf='twitter_output.csv', sep=',', encoding='utf-8')
