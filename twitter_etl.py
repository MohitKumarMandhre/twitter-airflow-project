import tweepy 
import pandas as pd 
import json 
from datetime import datetime
import s3fs 

def run_twitter_etl():

    access_key = "rzaO75uv0tKyFHMYM19gQvbYM"
    access_key_secret = "jNDIvcFtKSteeu83tQaIARYzMD812XDDxp7JU3QLkfQNYCVkn1"
    consumer_key = "1588059056597409792-psNJhyInw3xS71R2ipmlSe7BHyRXJW"
    consumer_key_secret = "Oa2b0UhioSSiJFIBgalPqbJPwNCDGwqglmkAhKzOMsqTl"

    # twitter authentication 
    auth = tweepy.OAuthHandler( access_key, access_key_secret)
    auth.set_access_token( consumer_key, consumer_key_secret)

    #creating an API object
    api = tweepy.API( auth)

    tweets = api.user_timeline(
        screen_name="@elonmusk",
        # 200 is the max allowed count of tweets
        count=200,
        # include retweets
        include_rts=False,
        # default 140 words
        tweet_mode='extended'
    )

    # print( tweets)

    tweets_list = [] 

    for tweet in tweets:
        text = tweet._json["full_text"]
        # print( text)
        refined_tweet = {
            'user': tweet.user.screen_name,
            'text': text,
            'favorite_count': tweet.favorite_count, 
            'retweet_count': tweet.retweet_count,
            'created_at': tweet.created_at
        }
        tweets_list.append( refined_tweet)

    df = pd.DataFrame( tweets_list)
    df.to_csv("s3://mkm-airflow-bucket001/elonmusk_data.csv")
