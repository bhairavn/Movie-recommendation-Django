# from passlib.hash import sha256_crypt
import psycopg2
from math import ceil
# from textanalysis import returnlabel
import re
# from stream_sites import stream_link

con = psycopg2.connect(
    host = "127.0.0.1",
    database = "movierecommender",
    user = "postgres",
    password = "admin",
    port="5432")
cur=con.cursor()

def carousel_data():
    cur.execute("select * from public.moviedatabase")
    mdata = cur.fetchall()
    n=len(mdata)
    temp=mdata.copy()
    nslides= n//4 +ceil((n/4)-(n//4))
    return (mdata,temp,len(mdata),len(temp),4)

import pandas as pd
def movie_name(data):
    df=pd.read_csv("Movierecommendation\closest_users.csv")
    df2=pd.read_csv("Movierecommendation\movie_image2.csv")
    name_lst=[]
    for i in data:
        t=df.Movieid2[df.Movieid1 == i[0]].values
        if len(t)>1:
            x=t[0]
        try:
            temp = df2[df2.index==x].values.tolist()
            name_lst.append([temp[0][0],temp[0][1],temp[0][2],temp[0][3],temp[0][4],temp[0][5]])
        except:
            print(" movie not found ")
    return name_lst
