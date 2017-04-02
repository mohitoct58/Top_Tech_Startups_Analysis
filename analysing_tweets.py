# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 12:33:00 2017

@author: Mohit
"""
import pandas as pd
from pandas import DataFrame
import tweepy
import csv
import matplotlib.pyplot as plt
import nltk
import sys
import networkx as nx
# For color mapping
import matplotlib.colors as colors
import matplotlib.cm as cmx



def authentication(filename = 'auth.k'):
    file = open(filename,'r')
    #all keys and tokens 
    ak = file.readlines()
    file.close()
    auth1 = tweepy.auth.OAuthHandler(ak[0].replace("\n",""), ak[1].replace("\n",""))
    auth1.set_access_token(ak[2].replace("\n",""), ak[3].replace("\n",""))
    api = tweepy.API(auth1,wait_on_rate_limit=True)
    return api
    
    
    
    
def draw_graph(graph):
    G=nx.Graph()
    startup_list = list()
    for edge in graph:
        G.add_edge(edge[0], edge[1])
        startup_list += [edge[0]]
    startup_list = set(startup_list)
    val_map = dict()
    for name,i in zip(startup_list,range(0,len(startup_list))):
        val_map[name] = 0.4 + i*0.05
        
    
    #graph_pos = nx.random_layout(G)
    
    
    pos=nx.spring_layout(G)
    
#    val_map = {'Sequoia Capital': 1.0,
#           'Tiger Global Management': 0.5714285714285714,
#           'SAIF Partners': 0.0}

    values = [val_map.get(node, 0.25) for node in G.nodes()]
    jet = cm = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=0, vmax=max(values))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    # Using a figure to use it as a parameter when calling nx.draw_networkx
    f = plt.figure(1)
    ax = f.add_subplot(1,1,1)
    for label in val_map:
        ax.plot([0],[0],
                color=scalarMap.to_rgba(val_map[label]),
                label=label)

    # Just fixed the color map
    nx.draw_networkx(G,pos, cmap = jet, vmin=0, vmax= max(values),
                     node_color=values,
                     with_labels=True,ax=ax)

    # Here is were I get an error with your code                                                                                                                         
    #nodes = nx.draw(G, cmap = plt.get_cmap('jet'), node_color = values)                                                                             

    # Setting it to how it was looking before.                                                                                                              
    plt.axis('off')
    f.set_facecolor('w')

    plt.legend(loc='upper left')


    f.tight_layout()
    plt.show()   
    
    
    
    
    
    
    
def activeness_of_top_10_startups():
        
    files1 = pd.read_csv('for_twitter_input.csv', names=["name","twitter_username","founded_in","website","category","investor"], encoding='cp1252')
    df1 = DataFrame(files1)
    df1 = df1.dropna()
    api = authentication('auth.k')
    list_of_top_10_startups = dict()
    only_userids_of_startups = list()
    print('start')
    
    for i in range(1,11):
        user_id = api.get_user(df1.iloc[i]['twitter_username']).id_str
        list_of_top_10_startups[user_id] = df1.iloc[i]['name']
        print(df1.iloc[i]['name'],user_id)
        only_userids_of_startups += [user_id]
    
    files2 = pd.read_csv('total_tweets_after_deleting_duplicates.csv', names=["userid","text","hashtags","usernames"], encoding='cp1252')
    df2 = DataFrame(files2)
    df2 = df2.dropna()
    
    csvFile = open('analytics/startups_tweets.csv','w')
    csvWriter = csv.writer(csvFile)
    #csvWriter.writerow(["name","userid","text"])
    for i in only_userids_of_startups:
        temp = df2[df2['userid']==i]
        for j in range(len(temp)):
            csvWriter.writerow([list_of_top_10_startups[i],temp.iloc[j]['userid'],temp.iloc[j]['text']])
        
    csvFile.close()
    
    
    files3 = pd.read_csv('analytics/startups_tweets.csv', names=["name","userid","text"], encoding='cp1252')
    df3 = DataFrame(files3)
    df3 = df3.dropna()
    
    g1 = df3.groupby( [ "name"] ).count()
    print(g1['text'])
    print(len(g1['text']))
    
    pos = list(range(len(g1['text'])))
    width = 0.2
    fig, ax = plt.subplots(figsize=(10,5))

    plt.bar(pos,
        #using df['text'] data,
        g1['text'],
        # of width
        width,
        # with alpha 0.5
        alpha=0.5,
        # with color
        color='#EE3224')
    ax.set_xticks([p + 1.5 * width for p in pos])
    ax.set_xticklabels(g1.index)
    plt.show()
    
    

def graph_visualization():
    files3 = pd.read_csv('analytics/startups_tweets.csv', names=["name","userid","text"], encoding='cp1252')
    df3 = DataFrame(files3)
    df3 = df3.dropna()
    
    graph = list()
    
    for i in range(len(df3)):
        text = nltk.word_tokenize(df3.iloc[i]['text'])
        li = nltk.pos_tag(text)
        for j in li:
            if j[1]=='NNP':#if (j[1]=='NN' or j[1]=='NNS') or j[1]=='NNP':
                if j[0].startswith('//'):
                    continue
                graph += [(df3.iloc[i]['name'],j[0])]
    
                          
    sys.stdout = open("analytics/name_noun_maping_of_startups.txt",'w')
    for i in graph:
        print(i[0]+","+i[1])
    sys.stdout = sys.__stdout__           
    
    files4 = pd.read_csv('analytics/name_noun_maping_of_startups.txt', names=["name","noun"], encoding='cp1252')
    df4 = DataFrame(files4)
    df4 = df4.dropna()
    
    graph = list()
    
    name_of_startups = df4['name'].unique().tolist()
    for i in name_of_startups:
        temp = df4[df4['name']==i]
        temp = temp.groupby(['noun']).count().sort_values(by='name')
        if len(temp)<10:
            for j in temp.index:
                graph += [(i,j)]
        else:
            for j in temp.index[-10:]:
                graph += [(i,j)]
    
    draw_graph(graph)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#activeness_of_top_10_startups()


graph_visualization()