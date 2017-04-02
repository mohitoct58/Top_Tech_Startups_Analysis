# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 09:58:16 2017

@author: Mohit
"""

import pandas as pd
from pandas import DataFrame
from collections import Counter 
import sys
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# For color mapping
import matplotlib.colors as colors
import matplotlib.cm as cmx


def findPaths(G,u,n,excludeSet = None):
    if excludeSet == None:
        excludeSet = set([u])
    else:
        excludeSet.add(u)
    if n==0:
        return [[u]]
    paths = [[u]+path for neighbor in G.neighbors(u) if neighbor not in excludeSet for path in findPaths(G,neighbor,n-1,excludeSet)]
    excludeSet.remove(u)
    return paths








def investors():
    files = pd.read_csv('for_twitter_input.csv', names=["name","twitter_username","founded_in","website","category","investors"], encoding='cp1252')
    df = DataFrame(files)
    df = df.dropna()
    
    list_of_top_10_startups_investors = list()
    for i in range(1,11):
        for j in df.iloc[i]['investors'].split(','):
            list_of_top_10_startups_investors += [(df.iloc[i]['name'],j)]

    sys.stdout = open('analytics/list_of_top_10_startups_investors.txt', 'w')
    for i in list_of_top_10_startups_investors:
        print(i[0],i[1])
        
    sys.stdout = sys.__stdout__
    list_for_graph_console = list()
    for i in range(1,len(df)):
        for j in df.iloc[i]['investors'].split(','):
            list_for_graph_console += [(df.iloc[i]['name'],j)]
    print(len(list_for_graph_console))
    return list_of_top_10_startups_investors,list_for_graph_console



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
    
    
    
#    val_map = {'Sequoia Capital': 1.0,
#           'Tiger Global Management': 0.5714285714285714,
#           'SAIF Partners': 0.0}
#
#    values = [val_map.get(node, 0.25) for node in G.nodes()]
#
#    nx.draw(G, cmap=plt.get_cmap('jet'), node_color=values)
    
    
    
    #nx.draw_networkx_nodes(G, graph_pos, node_size=10, node_color='blue', alpha=0.3)
    #nx.draw_networkx_edges(G, graph_pos, edge_color='black')
    #nx.draw_networkx_labels(G, graph_pos, font_size=6, font_family='sans-serif')
    
    #plt.show()
    
    #plt.savefig('analytics/pic.png')
    
    
def querying_graph(graph,investors_name):
    print('Name of Investors:')
    for i in investors_name: 
        print(i.encode('cp850','replace').decode('cp850'),end=', ')
    print()
    G=nx.Graph()
    for edge in graph:
        G.add_edge(edge[0], edge[1])
    choice = True
    
    while(choice):
        targeted_company = input("Enter the name of the company:")
        startup_name = input("Enter the name of the startup:")
        distance_length = int(input("Enter the distance length(eg, 3)"))
        distance_length = abs(distance_length)
        paths = findPaths(G,targeted_company,distance_length)
        solutions = list()
        for i in paths:
            temp = i[-1].lower()
            if temp==startup_name:
                solutions += [i]
        if len(solutions)==0:
            print("Sorry no feasible way to approach that company.\nTry to increase the length." )
        else:
            print('feasible ways:')
            for i in solutions:
                print(i)
        c = input('Repeat It(Y/N):')
        if c!='Y':
            choice = False
        
def total_investors_name():
    files = pd.read_csv('for_twitter_input.csv', names=["name","twitter_username","founded_in","website","category","investors"], encoding='cp1252')
    df = DataFrame(files)
    df = df.dropna()
    investors_name = list()
    for i in range(1,len(df)):
        investors_name += df.iloc[i]['investors'].split(',')
    investors_name = set(investors_name)
    return investors_name
    
    
def analysis_of_twitter_friends():
    files = pd.read_csv('twitter_output.csv', names=["name","twitter_username","friends_count","friends","count"], encoding='cp1252')
    df = DataFrame(files)
    df = df.dropna()
    
    username_to_startup_mapping = dict()
    
    for i in range(0,len(df)):
        for j in df.iloc[i]['friends'].split(','):
            username_to_startup_mapping[j] = username_to_startup_mapping.get(j,[]) + [df.iloc[i]['name']]

    username_to_frequency_mapping = list()
    for i in username_to_startup_mapping.items():
        username_to_frequency_mapping += [(i[0],len(i[1]))]

    username_to_frequency_mapping.sort(key = lambda x: x[1])
    
    sys.stdout = open('analytics/username_frequency.txt', 'w')
    for i in username_to_frequency_mapping:
        print(i[0],i[1])
    sys.stdout = open('analytics/top_frequencies.txt', 'w')
    start = round(len(username_to_frequency_mapping)*0.999)
    end = len(username_to_frequency_mapping)
    print(start,end)
    graph = list()
    for i in range(start,end):
        print(username_to_frequency_mapping[i][0],username_to_frequency_mapping[i][1])
        for j in username_to_startup_mapping[username_to_frequency_mapping[i][0]]:
            graph += [(username_to_frequency_mapping[i][0],j)]
    sys.stdout = sys.__stdout__
    
    
    
    G=nx.Graph()
    username_list = list()
    for edge in graph:
        G.add_edge(edge[0], edge[1])
        username_list += [edge[0]]
    username_list = set(username_list)
    val_map = dict()
    color = np.linspace(0.2,0.9,len(username_list)).tolist()
    for name,i in zip(username_list,color):
        val_map[name] = i
        
    
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
    
    
  
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
list_of_top_10_startups_investors, list_for_graph_console = investors()    

#querying_graph(list_for_graph_console, total_investors_name())

graph = list_of_top_10_startups_investors
draw_graph(graph)

#analysis_of_twitter_friends()



















