
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import string
import pandas as pd

consumer_key = "0NtWOiVa3QVTGeS6GHPBHKaPY"
consumer_secret_key = "0FdK4e5qgSPqXbuKXLZXGlHqrPWPmRMc5czE70wGPMpk5RSzOw"
access_token = "1585332354481995777-4lxO5nMMDg8AYftW1T3ktggRWghoGB"
access_secret_key = "trJUeywlj3prYQGQUaxIETA8mK7iXqolcwIGodQ6NPzcP"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_secret_key)
 
api = tweepy.API(auth)

# 1
screen_name = "sundarpichai"
user = api.get_user(screen_name)
print(user.name)
print(user.screen_name)
print(user.id)
print(user.location)
print(user.description)
print(user.followers_count)
print(user.friends_count)
print(user.statuses_count)
print(user.url)

#2
users = ["sundarpichai", "tim_cook"]
user_Data = {}
for usr in users:

  user_Data[usr] = {}

  friends_list = []
  for friend in api.friends(usr):
    friends_list.append(friend.screen_name)
  user_Data[usr]["friends"] = friends_list

  followers_list = []
  for follower in tweepy.Cursor(api.followers, usr).items(20):
	  followers_list.append(follower.screen_name)
  user_Data[usr]["followers"] = followers_list
  

print(user_Data)

# 3a
query = "Ohio weather"
tweets = tweepy.Cursor(api.search, q=query).items(50)

all_tweets_keywords = [tweet.text for tweet in tweets]
print(all_tweets_keywords)

# 3b
query = "Ohio weather"
geo= "39.758949 -84.191605 25mi"
tweets = tweepy.Cursor(api.search, q=query,geo_code=geo).items(50)

all_tweets_location = [tweet.text for tweet in tweets]
print(all_tweets_location)

# 4

class Twitter(object):

  def __init__(self, api):
    try:
      self.api = api
    except:
      print("Error: Authentication Failed")

  def clean_tweet(self, x):
    x = x.lower()
    x = x.encode('ascii', 'ignore').decode()
    x = re.sub(r'https*\S+', ' ', x)
    x = re.sub(r'@\S+', ' ', x)
    x = re.sub(r'#\S+', ' ', x)
    x = re.sub(r'\'\w+', '', x)
    x = re.sub('[%s]' % re.escape(string.punctuation), ' ', x) 
    x = re.sub(r'\s{2,}', ' ', x)
    return x

  def tweets_sentiment(self, tweet):

    analysis = TextBlob(self.clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
      return 'positive'
    elif analysis.sentiment.polarity == 0:
      return 'neutral'
    else:
      return 'negative'

  def get_tweets(self, query, count = 10):
    tweets = []
    try:
      fetched_tweets = self.api.search(q = query, count = count)
      for tweet in fetched_tweets:
        parsed_tweet = {}
        parsed_tweet['text'] = tweet.text
        parsed_tweet['sentiment'] = self.tweets_sentiment(tweet.text)
        if tweet.retweet_count > 0:
          if parsed_tweet not in tweets:
            tweets.append(parsed_tweet)
        else:
          tweets.append(parsed_tweet)
      return tweets

    except tweepy.TweepError as e:
      print("Error : " + str(e))

def main():
  a = Twitter(api)
  tweets = a.get_tweets(query = 'sundar pichai', count = 200)
  ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
  ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
  print("Positive tweets: {} %".format(100*len(ptweets)/len(tweets)))
  print("Negative tweets: {} %".format(100*len(ntweets)/len(tweets)))
  print("Neutral tweets: {} % ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))

  print("\n\nPositive tweets:")
  for tweet in ptweets[:10]:
    print(tweet['text'])

  print("\n\nNegative tweets:")
  for tweet in ntweets[:10]:
    print(tweet['text'])

if __name__ == "__main__":
  main()