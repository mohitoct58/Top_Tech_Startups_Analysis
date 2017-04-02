# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 17:45:50 2017

@author: Mohit
"""
import csv
import tweepy
import time
import pandas as pd
from pandas import DataFrame

# AUTHENTICATION (OAuth)
def authentication(filename = 'auth.k'):
    file = open(filename,'r')
    #all keys and tokens 
    ak = file.readlines()
    file.close()
    auth1 = tweepy.auth.OAuthHandler(ak[0].replace("\n",""), ak[1].replace("\n",""))
    auth1.set_access_token(ak[2].replace("\n",""), ak[3].replace("\n",""))
    api = tweepy.API(auth1,wait_on_rate_limit=True)
    return api

#for limiting the transfer amount
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print("sleeping")
            time.sleep(15 * 60)
            

api = authentication('auth.k')


#for writing the list of friends
csvFile = open('twitter_output.csv','a')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["name","twitter_username","friends_count","friends","count"])



#for reading the inputs for twitter 
files = pd.read_csv('for_twitter_input.csv', names=["name","twitter_username","founded_in","website","category","investors"], encoding='cp1252')
df = DataFrame(files)
df = df.dropna()

#leaving those company that dont have twitter account
for i in range(1,len(df)):
    username = df.iloc[i]["twitter_username"]
    if username=="not_applicable":
        continue
    print("starting for:",username)
    friends_count = api.get_user(username).friends_count
    print(friends_count)
    list_of_friends = list()
    count = 0
    try:
        for friend in limit_handled(tweepy.Cursor(api.friends, screen_name = username).items()):
            list_of_friends += [friend.screen_name]
            count += 1
            print(df.iloc[i]["twitter_username"],count,friend.screen_name)
        
    
    finally:
        friends = ",".join(list_of_friends)
        csvWriter.writerow([df.iloc[i]["name"],df.iloc[i]["twitter_username"],friends_count,friends,count])
        
csvFile.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    