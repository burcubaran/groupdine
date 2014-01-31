import os
import subprocess
import urllib
import json
import requests
import Image
from os import listdir
from os.path import isfile, join

from pandas import *
import pandas.io.sql as psql
import MySQLdb as mdb

con=mdb.connect(host="127.0.01", user='root', db='world_innodb')
city={'Mountain View':'restMV', 'San Jose':'restSJ', 'Palo Alto':'restPA', 
      'Redwood City':'restRC', 'Cupertino':'restC', 'Santa Clara':'restSC',
      'San Mateo':'restSM', 'South San Francisco':'restSSF','Daly City':'restDC', 'San Leandro':'restSL', 
      'Hayward':'restH', 'Los Gatos':'restLG', 'Fremont':'restF', 'Milpitas':'restM',
      'Oakland':'restOa', 'Berkeley':'restB'}



#get the location id by the name and geolocation of the restaurant.

def locid(n,x):
    req=requests.get("https://api.instagram.com/v1/locations/search?lat="+str(x[0])+"&lng="+str(x[1])+"&access_token=232690335.f8c47bd.caf347ce037a42c29805a4f389aaf788&distance=500")
    js=req.json()
    d=dict(js)
    d=d['data']
    i=0
    while i < len(d):
        if n in d[i]['name']:
            return d[i]['id']
        else:
            i+=1
    else:
        return 'noname'

#get the jpeg source of the photos of the restaurants by the location id

def asilurl(x):
    req=requests.get("https://api.instagram.com/v1/locations/"+str(x)+"/media/recent?access_token=232690335.f8c47bd.caf347ce037a42c29805a4f389aaf788")
    js=req.json()
    d=dict(js)
    d=d['data']
    fotourl=[]
    for i in d:
        fotourl.append(i['images']['standard_resolution']['url'])
    return fotourl


#get all the photos of the restaurant

def foto(res,y):
    li=[]
    res1="""SELECT lat, longi FROM %s WHERE name= "%s" """ %(city[y], res)
    a=psql.frame_query(res1, con=con)
    b=a.values.tolist()
    if locid(res,[b[0][0], b[0][1]]) == 'noname':
       return li
    else:
        g=locid(res, [b[0][0], b[0][1]])
        return asilurl(g)
    

        