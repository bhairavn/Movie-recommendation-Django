import urllib.request, urllib.parse, urllib.error
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
def movie_summary(name):
    #name = name.split(" ").join("+")
    url = "https://www.google.com/search?q=imdb"+name
    req = requests.get(url)
    s = BeautifulSoup(req.text, "html.parser")

    links = s.find_all('a')
    try:
        for link in links:
            y = re.findall("(<a .*imdb.com.*</a>)",str(link))
            if (y!=[]):
                break

        if (y==None):
            link = 'Not found'


        link_parts = str(link).split('/')

        imdb_link = "http://"+link_parts[3]+'/'+link_parts[4]+'/'+link_parts[5]+'/'
        url3 = imdb_link

        req2 = requests.get(url3)
        s2 = BeautifulSoup(req2.text, "html.parser")
        #<div class="ipc-html-content ipc-html-content--base"><div>
        #              Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.
        #      </div></div>
        summary_class = s2.find_all('div',{'class':"summary_text"})
        summary_class = summary_class[0]
        summary_text = str(summary_class)
        summary_text = re.findall("(.*)", summary_text)
        summary_text = summary_text[2].strip()

        try:
            director_class = s2.find_all('div',{'class':"credit_summary_item"})
            director_class = str(director_class[0])
            director_name = re.findall(">(.*)</a>", director_class)
            director_name = director_name[0]
            director_name = director_name.split("</a>")
            director_name = director_name[0]
        except:
            director_name = "Not found"
        try:    
            table_class = s2.find_all('table',{'class':"cast_list"})
            table_class = table_class[0]
            body = table_class.find_all("tr")
            cast_list = []
            for person in body:
                actor_names = re.findall("<img alt=(.*) class=", str(person))
                if len(actor_names)>0:
                    cast_list.append(actor_names)
                    cast_list=','.join(cast_list)
        except:
            cast_list="Not Found"

        #actor_names = re.findall(">(.*)</a>", table_class)
        #print(actor_names)

        return(summary_text.strip(), director_name, cast_list)
    except:
        return("sorry description for this movie not found","-","-")

#description = .find_all('div')
#print(description)'''
# name = input("Enter name of the movie")
# print(movie_summary(name))