# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 10:48:55 2017

@author: Mohit
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import pandas as pd
from pandas import DataFrame



#download the content to a file 
def download_tabular_data():
    temp = urlopen('https://profiles.yourstory.com/embed/report/india-100-2016.html').read()
    soup = BeautifulSoup(temp,"html.parser")
    file = open("tabular_info_of_website.txt","w")
    file.write(soup.prettify().encode('cp850','replace').decode('cp850'))
    file.close()
    

#scraping data from the downloaded file
def scraping_main():
    file = open("tabular_info_of_website.txt","r")
    csvFile = open('data.csv','w')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["name","link_in_site","web_rank","brand_rank","mobile_rank","funding_rank","readers_rank"])
    html = file.read()
    html = BeautifulSoup(html,"html.parser")
    table_body = html.find("tbody")
    table_rows = table_body.find_all("tr")
    for i in table_rows:
        table_data = i.find_all("td")
        name = table_data[2].get_text().strip()
        link_in_site = "https://profiles.yourstory.com"+table_data[2].find("a").get('href')
        web_rank = table_data[3].get_text().strip()
        brand_rank = table_data[4].get_text().strip()
        mobile_rank = table_data[5].get_text().strip()
        funding_rank = table_data[6].get_text().strip()
        readers_rank = table_data[7].get_text().strip()
        csvWriter.writerow([name,link_in_site,web_rank,brand_rank,mobile_rank,funding_rank,readers_rank])
    file.close()
    csvFile.close()
    
    
#scraping the pages of the from the stored links(link_in_site) 
def scraping_sub_pages():
    
    #for mapping company to their twitter username
    csvFile = open('for_twitter_input.csv','w')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["name","twitter_username","founded_in","website","category","investors"])
    
    #for reading the main page data
    files = pd.read_csv('data.csv', names=["name","link_in_site","web_rank","brand_rank","mobile_rank","funding_rank","readers_rank"], encoding='cp1252')
    df = DataFrame(files)
    df = df.dropna()
    
    for i in range(1, len(df)):
        print(df.iloc[i]["link_in_site"])  
        temp = urlopen(df.iloc[i]["link_in_site"]).read()
        soup = BeautifulSoup(temp,"html.parser")
        category = soup.find("span",class_ = "profile-tag").get_text()
        info1 = soup.find_all("div",class_="row padding-15")
        
        for j in info1:
            heading = j.find("div",class_="col-lg-2 col-md-2 col-sm-2 col-xs-4 other-left-bg").get_text()
            value = j.find("div",class_="col-lg-5 col-md-5 col-sm-5 col-xs-8")
            if(heading=="Founded In"):
                founded_in = value.get_text()
                print('Founded In:',value.get_text())
            elif(heading=="Website"):
                website = value.find("a").get("href")
                print('Website:',value.find("a").get("href"))
            elif(heading=="Social"):
                twitter_username = value.find_all("a")[1].get("href").split('/')[-1]
                print('Twitter:',value.find_all("a")[1].get("href").split('/')[-1])
                if twitter_username=="":
                    twitter_username = 'not_applicable'
        

        info2 = soup.find_all("div",class_="editContent text-center margin-top-15 gallery-cell-text")
        investors_list = list()
        for j in info2:
            try:
                investor_name = j.div['title']
                investors_list += [investor_name]
            except:
                pass
        investors = ",".join(investors_list)
        print(investors)
        csvWriter.writerow([df.iloc[i]['name'],twitter_username,founded_in,website,category,investors])
        print('\n')
        
    csvFile.close()



    
download_tabular_data()    
scraping_main()
scraping_sub_pages()    














