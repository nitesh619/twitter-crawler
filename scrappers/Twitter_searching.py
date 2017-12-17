import datetime
import json

import pandas as pd
import tweepy

settings = json.load(open('settings.json'))
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


def get_search_place(config):
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


def get_search_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return date
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD")


def get_result_type(result_type):
    if result_type in ['mixed', 'recent', 'popular']:
        return result_type
    else:
        print("result_type can only be {0}, {1} or {2}.".format('mixed', 'recent', 'popular'))


# search tweet's for keywords
def search_twitter(**kwargs):
    search_count = 0
    print("searching for: " + kwargs['query'])

    with open('search.json', 'w') as f:
        for status in tweepy.Cursor(api.search, q=kwargs['query'],
                                    count=tweet_per_query,
                                    since=kwargs['since'], until=kwargs['until'],
                                    result_type=kwargs['result_type']).items():
            tweet_json = status._json
            f.writelines(json.dumps(tweet_json, indent=4, sort_keys=True))
            user = tweet_json['user']
            lead_names.append(user['name'])
            lead_handles.append("@" + user['screen_name'])
            lead_bio.append(user['description'])
            lead_verified.append(user['verified'])
            search_count += 1
        search_leads['Name'] = pd.Series(lead_names)
        search_leads['Handle'] = pd.Series(lead_handles)
        search_leads['Verified'] = pd.Series(lead_verified)
        search_leads['Bio'] = pd.Series(lead_bio)
        search_leads['Profile_Link'] = profile_link_prefix + search_leads['Handle'].map(lambda x: str(x)[1:])
        print('Found {0} matching tweets.'.format(search_count))


def prepare_search_query(config):
    since = None
    until = None
    result_type = None
    place = None
    if config['since']:
        since = get_search_date(config['since'])
    if config['until']:
        until = get_search_date(config['until'])
    if config['result_type']:
        result_type = get_result_type(config['result_type'])
    if config['country'] or config['city']:
        place = "place:" + get_search_place(config) + " "
    return since, until, result_type, place if place else ""


since, until, result_type, place = prepare_search_query(config)
for key in keywords['Keywords'].append(keywords['HashTags']).head():
    query = place + key
    search_twitter(query=query, since=since, until=until, result_type=result_type)

search_leads.drop_duplicates(subset=['Handle'], keep=False, inplace=True)
search_leads.reset_index(drop=True, inplace=True)
#
search_leads.to_csv(path_or_buf='twitter_output.csv', sep=',', encoding='utf-8')
