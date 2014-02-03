import os
from pandas import *
import pandas.io.sql as psql
import MySQLdb as mdb
import operator

con=mdb.connect(host="127.0.01", user='root', db='world_innodb')



sql="""SELECT name, category, prange FROM rest"""

df=psql.frame_query(sql, con=con) 
city={'Mountain View':'restMV', 'San Jose':'restSJ', 'Palo Alto':'restPA', 
      'Redwood City':'restRC', 'Cupertino':'restC', 'Santa Clara':'restSC',
      'San Mateo':'restSM', 'South San Francisco':'restSSF','Daly City':'restDC', 'San Leandro':'restSL', 
      'Hayward':'restH', 'Los Gatos':'restLG', 'Fremont':'restF', 'Milpitas':'restM',
      'Oakland':'restOa', 'Berkeley':'restB'}


def giverest(rests,y):

#list of list of restaurants with properties (category, price) 
#from the list of locations that the username has been.
  
    for listi in rests:
        for rest in listi:
            listi[listi.index(rest)]=rest.title()
    
#grading the categories and prices    
    
    val_cat={}
    val_price={}    
    
    already=[]
    for listi in rests: 
        bb=df[df['name'].isin(listi)]
        indexlength=len(bb.index)


        for i in range(indexlength):
            prop=bb.iloc[i].tolist()
            already.append(prop[0])
            if prop[1] in val_cat.keys():
                val_cat[prop[1]]+=int(1)
            else:
                val_cat[prop[1]]=1
            if prop[2] in val_price.keys():
                val_price[prop[2]]+=1
            else:
                val_price[prop[2]]=int(1)
        
    n=max(val_cat.values())
    m=max(val_price.values())

 
#getting the names of the restaurants with the highest graded
#category and price        
        
    listcat=[]
    listprice=[]
       
    for i in val_cat.keys():
        if val_cat[i]==n:
            listcat.append(i)
    
    for i in val_price.keys():
        if val_price[i]==m:
            listprice.append(i)

#getting the names of the restaurants with the highest graded
#category and price and making the final list
        
    final=[]
    tochoose={} 
    for i in listcat:
        for j in listprice:
            sql1="""SELECT Name, rank FROM %s WHERE category= '%s' AND prange= '%s'""" % (city[y],i,j)
            a=psql.frame_query(sql1, con=con)
            b=a.values.tolist()
            tochoose[(i,j)]=b[0][0]
    
    chosen=max(tochoose.iteritems(), key=operator.itemgetter(1))[0]         
    
    sql1="""SELECT Name FROM %s WHERE category= '%s' AND prange= '%s'""" % (city[y], chosen[0], chosen[1])           
    a=psql.frame_query(sql1, con=con)
    b=a.values.tolist()
 
 #making the final list and the ranking dictionary                    
    for i in b:
        final.append(str(i[0]))
                   
   
   
  #subtracting from the final list the restaurants that had already been   
    for i in range(indexlength):
        prop=list(bb.iloc[i])
        final=[x for x in final if x not in already]  
   
   
   #ordering with respect to the highest rank and getting the first 3 of them.                              
            #final=sorted(dicrank, key=dicrank.__getitem__, reverse=True)
        
        
    return final


#function that takes the lat and longi of the restaurant
        
def latlong(res,y):
    sql1="""SELECT lat, longi FROM %s WHERE name= "%s" """ % (city[y],res)
    a=psql.frame_query(sql1, con=con)
    b=a.values.tolist()
    return b[0]

#changing the name of the category.

def catfunc(x):
    if x=='cat1':
        return 'American Cuisine'
    elif x=='cat2':
        return 'Asian Cuisine'
    elif x=='cat3':
        return 'Latin American Cuisine'
    elif x=='cat4':
        return 'Cafes'
    elif x=='cat5':
        return'Mediterranean Cuisine'
    elif x=='cat6':
        return 'Ethnic Cuisine'   

