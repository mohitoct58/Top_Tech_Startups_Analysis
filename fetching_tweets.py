# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 17:47:56 2017

@author: Mohit
"""

import csv
import pandas as pd
from pandas import DataFrame
import unidecode
import json
import sys
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


#for merging many files or for filtering only required columns
def merging_all_tweets():
    csvFile = open('total_tweets.csv','a', encoding='cp1252')
    csvWriter = csv.writer(csvFile)
    #csvWriter.writerow(["user_id","text","hashtags","user_mentions"])
        
    
    tweets_data_path = 'stream.txt'
    
    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    temp = 0
    count = 0
    l = 0
    for line in tweets_file:
        count += 1
        try:
            tweet = json.loads(line)
            xxx = tweet['user']['id']
            tweets_data.append(tweet)
            l +=1
        except:
            temp +=1
            #print("error")
            continue
    #print(count)
    #print(temp)
    #print(l)
    tweets = pd.DataFrame()
    tweets['user_id'] = list(map(lambda tweet: tweet['user']['id'], tweets_data))
    tweets['text'] = list(map(lambda tweet: unidecode.unidecode(tweet['text']), tweets_data))
    tweets['hashtags'] = list(map(lambda tweet: [str(i).encode('cp850','replace').decode('cp850') for i in tweet['entities'][u'hashtags']],tweets_data)) 
    tweets['user_mentions'] = list(map(lambda tweet: [str(i).encode('cp850','replace').decode('cp850') for i in tweet['entities'][u'user_mentions']],tweets_data)) 
    
    for i in range(len(tweets)):
        a = tweets.iloc[i]['user_id']
        b = tweets.iloc[i]['text'].encode('cp850','replace').decode('cp850')
        c = tweets.iloc[i]['hashtags']
        d = tweets.iloc[i]['user_mentions']
        csvWriter.writerow([a,b,c,d])
    
        
    csvFile.close()



def dropping_duplicates():
    files = pd.read_csv('total_tweets.csv', names=["user_id","text","hashtags","user_mentions"], encoding='cp1252')
    df = DataFrame(files)
    df = df.dropna()
    df = df.drop_duplicates()
    csvFile = open('total_tweets_after_deleting_duplicates.csv','a', encoding='cp1252')
    csvWriter = csv.writer(csvFile)
    for i in range(len(df)):
        a = df.iloc[i]['user_id']
        b = df.iloc[i]['text'].encode('cp850','replace').decode('cp850')
        c = df.iloc[i]['hashtags']
        d = df.iloc[i]['user_mentions']
        csvWriter.writerow([a,b,c,d])
    
        
    csvFile.close()
    
    
    
    
def authentication(filename = 'auth.k'):
    file = open(filename,'r')
    #all keys and tokens 
    ak = file.readlines()
    file.close()
    auth1 = tweepy.auth.OAuthHandler(ak[0].replace("\n",""), ak[1].replace("\n",""))
    auth1.set_access_token(ak[2].replace("\n",""), ak[3].replace("\n",""))
    api = tweepy.API(auth1,wait_on_rate_limit=True)
    return auth1,api
    
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)   
    
#fetching tweets for only top 10 companies    
def getting_all_tweets(authentication):    
    l = StdOutListener()
    sys.stdout = open('stream.txt', 'w')
    stream = Stream(authentication, l)
    files = pd.read_csv('for_twitter_input.csv', names=["name","twitter_username","founded_in","website","category","investors"], encoding='cp1252')
    df = DataFrame(files)
    df = df.dropna()
    list_top_10 = [df.iloc[i]['twitter_username'] for i in range(1,11)]
    try:
        stream.filter(track=list_top_10)
    except:
        pass


#auth,api = authentication('auth.k')
#getting_all_tweets(auth)
#merging_all_tweets()
#dropping_duplicates()
    
    
    
    
    
    
    
    
    
    
    
    
    
    