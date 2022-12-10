import requests
import csv
import re
import sys

def remove_newline(str):
    return re.sub('[\n]', '', str)


def clean_tweets(tweet):
    # this function cleans the given string by removing
    # a) any word after @,
    # b) any single character that is not a digit or a letter, and
    # c) any links (words with :// in it)
    return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+://\S+)", " ", tweet).split())


def get_tweets_by_tag(tagname, count):
    url = "https://api.twitter.com/2/tweets/search/recent"
    querystring = {
        "query": f"#{tagname} -is:retweet lang:en is:verified",
        "max_results": 100,
        "tweet.fields": "created_at"
    }
    headers = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAGX%2BjwEAAAAAm%2Bt7HbyzO08XzTd51Q0Z%2FNS6ZOI"
                         "%3DrV1tF4a7NvrV3EK1r2UAXb4w6Nvofr4GJ5gqP0oqKl0QnsDrgD"
    }
    tweets = []
    page_count = 0
    while page_count == 0 or (page_count < (count // 100) and querystring.get("next_token", None) is not None):
        page_count += 1
        response = requests.get(url, headers=headers, params=querystring)
        querystring["next_token"] = response.json()["meta"].get("next_token", None)
        data = response.json().get("data", None)

        tweets += [(i["id"], remove_newline(i["text"]), i["created_at"]) for i in data] if data is not None else []

    return tweets


if __name__ == "__main__":
    tweet_data = get_tweets_by_tag("COVID19", int(sys.argv[1]))
    with open('covid_tweets.csv', 'w') as out:
        fw = csv.writer(out)
        fw.writerow(['id', 'text', 'created_at'])
        for row in tweet_data:
            fw.writerow(row)
