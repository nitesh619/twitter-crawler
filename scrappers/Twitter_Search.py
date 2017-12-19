import datetime
import json

import pandas as pd
import tweepy

try:
    settings = json.load(open('settings.json'))
    keywords = pd.read_csv('keywords.csv')
except Exception, e:
    print 'Problem with settings.json or keywords.csv: ' + str(e)
    print 'Aborting searching...'
    exit(-1)

profile_link_prefix = 'https://twitter.com/'
leads = {'Name': [], 'Handle': [], 'Verified': [], 'Profile_Link': [], 'Country': [], 'City': [], 'Bio': []}

credentials = settings['credentials']
config = settings['search_configuration']

API_KEY = credentials["consumer_key"]
API_SECRET = credentials["consumer_secret"]
ACCESS_TOKEN = credentials['access_token']
ACCESS_SECRET = credentials['access_secret']

tweet_per_query = config["tweets_per_query"] or 50

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

    query = config['country'] or config['city']
    granularity = 'country' if config['country'] else 'city'
    places = api.geo_search(query=query, granularity=granularity)

    if len(places) <= 0:
        print("City or Country you entered doesn't exist.")
        exit(-1)
    else:
        return places[0].id


def get_search_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return date
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD. Using defaults!")


def get_result_type(result_type):
    if result_type in ['mixed', 'recent', 'popular']:
        return result_type
    else:
        print("result_type can only be {0}, {1} or {2}. Using defaults!".format('mixed', 'recent', 'popular'))


# search tweet's for keywords
def search_twitter(**kwargs):
    print("searching for: " + kwargs['query'])

    search_count = 0
    for status in tweepy.Cursor(api.search, q=kwargs['query'],
                                count=tweet_per_query,
                                since=kwargs['since'],
                                until=kwargs['until'],
                                result_type=kwargs['result_type']).items():
        tweet_json = status._json
        user = tweet_json['user']
        place = tweet_json['place']
        screen_name = "@" + user['screen_name']

        leads['Name'].append(user['name'])
        leads['Handle'].append(screen_name)
        leads['Bio'].append(user['description'])
        leads['Verified'].append(user['verified'])
        leads['Country'].append(place['country'] if place else "")
        leads['City'].append(place['name'] if place else "")
        leads['Profile_Link'].append(profile_link_prefix + screen_name[1:])
        search_count += 1
    print('Found {0} matching tweets.'.format(search_count))


def prepare_search_query(config):
    since = get_search_date(config['since']) if config['since'] else None
    until = get_search_date(config['until']) if config['until'] else None
    result_type = get_result_type(config['result_type']) if config['result_type'] else None
    if config['country'] or config['city']:
        place = "place:" + get_search_place(config) + " "
    else:
        place = None
    return since, until, result_type, place or ""


since, until, result_type, place = prepare_search_query(config)
for key, tag in zip(keywords['Keywords'], keywords['HashTags']):
    query = place + key.strip() + " OR " + tag.strip()
    search_twitter(query=query, since=since, until=until, result_type=result_type)

search_leads = pd.DataFrame.from_dict(leads)
search_leads.drop_duplicates(subset=['Handle'], keep=False, inplace=True)
search_leads.reset_index(drop=True, inplace=True)

try:
    filter_handles = pd.read_csv('filter.csv')
    search_leads = search_leads[~search_leads.Handle.isin(filter_handles.Handle)]
except:
    print 'No filter csv found!'

print 'Total {} tweets found'.format(len(leads['Handle']))
print '{} unique twitter handles found.'.format(search_leads.shape[0])
# sort column's order
search_leads = search_leads[['Name', 'Handle', 'Verified', 'Profile_Link', 'Country', 'City', 'Bio']]
# Save search result's to file.
search_leads.to_csv(path_or_buf='twitter_search_result.csv', sep=',', encoding='utf-8', index=False)
# Author - Nitesh Jain
