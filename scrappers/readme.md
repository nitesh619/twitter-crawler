# Search Tweets Programatically
A project written in Python to search for keywords and hashTags in tweets with Twitter Official API and Web Crawling.

## Details
Twitter Official REST API provide excellent python library tweepy for accessing your twitter account using python script. You can search Twitter for tweet's with keywords, place, date etc.

Twitter Official API has the bother limitation of time constraints, you can't get older tweets than a week. We have used online available 'got' library to get tweets older than a week.
We get the best advantage of Twitter Search on browsers, it can search the deepest oldest tweets.


## Prerequisites
The scripts assumes using Python 2.x. 

Expected package dependencies are listed in the "requirements.txt" file for PIP, you need to run the following command to get dependencies:
```
pip install -r requirements.txt
```

## Components
- **Twitter_Crawler_OldTweets** Python script to get tweet's older than a week. It takes csv with keywords and HashTags as input and search twitter according to configuration provided in settings.json.

- **Twitter_Search** Python script to get tweet's using official twitter API. It takes csv with keywords and HashTags as input and search twitter according to configuration provided in settings.json.

- **Exporter:** Output files.
  - **Twitter_Search** exports result to a csv file named **"twitter_search_result.csv"**.
  - **Twitter_Crawler_OldTweets** exports result to a csv file named **"old_tweets.csv"**.

- **Importer:** Input Files
  - **Twitter_Search** and **Twitter_Crawler_OldTweets** reads keywords/hasTags from a csv file named **"keywords.csv"**. It must have two columns:
    - **Keywords**: List of keyword's to search twitter. Include your keyword in quotes if need to search the whole word. eg: "supply chain"
    - **HashTags**: List of #HashTag's to search twitter. eg: "#Trump" 
  - **filter.csv** file contains list of twitter handles that should be excluded from search output. It must have one column:
    - **Handle**: List of excluded twitter user handles.


## Generating Credentials (Key and Tokens)

- Login to your twitter account.
- Open the Twitter App Console(https://apps.twitter.com/).
- Click "Create New App" if no Twitter Apps are registered yet with your account.
- Fill Application Details in the form. Enter any url in "website" input box.
- Check "Developer Agreement" and click "create new twitter application" button.
- Click on "Keys and Access Tokens" Tab.
- Click on "Create my Access Token" button to generate tokens.


## Settings.json

- **credentials:** Twitter API keys and tokens to authenticate using Twitter gateway.
  - **consumer_key** (str): Copy "Consumer Key (API Key)" value under Application Settings.
  - **consumer_secret** (str): Copy "Consumer Secret (API Secret)" value under Application Settings.
  - **access_token** (str): Copy "Access Token" value under Your Access Token.
  - **access_secret** (str): Copy "Access Token Secret" value under Your Access Token.
  
- **old_tweet_configuration:** A collection of search parameters to be used together with **Twitter_Crawler_OldTweets**.
  - **max_tweets** (int): The maximum number of tweets to be retrieved. If this number is unsetted or lower than 1 all possible tweets will be retrieved.
  - **since** (str. "yyyy-mm-dd"): A lower bound date to restrict search.
  - **until** (str. "yyyy-mm-dd"): An upper bound date to restrist search.
  - **top_tweets** (boolean): True, if you only want to include top tweet's in search result.

- **search_configuration:** A collection of search parameters to be used together with **Twitter_Search**.
  - **result_type** (str): Optional. Specifies what type of search results you would prefer to receive. The current default is “mixed.” Valid values include:
      - **mixed**: include both popular and real time results in the response.
      - **recent**: return only the most recent results in the response
      - **popular**: return only the most popular results in the response.
  - **since** (str. "yyyy-mm-dd"): A lower bound date to restrict search.
  - **until** (str. "yyyy-mm-dd"): Returns tweets created before the given date. Keep in mind that no tweets will be found for a date older than one week.
  - **country** (str): Returns tweets by users located within a given country.
  - **city** (str): Returns tweets by users located within a given city.