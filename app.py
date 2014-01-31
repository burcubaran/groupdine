from os.path import expandvars
import sys
import traceback
import os


from flask import Flask, render_template, send_from_directory, request, redirect, flash, json, jsonify, url_for
import urllib
import json
import requests
from pandas import *
import pandas.io.sql as psql
import MySQLdb as mdb



import getlocations
from getlocations import *
import restsuggestions
from restsuggestions import *
import takefoto
from takefoto import *

#initialization
app=Flask(__name__)
app.config.update(DEBUG=True)
app.secret_key = "skjdhfjljdfhdjf,jf,xfjg"

#controllers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

#@app.errorhandler(404)
#def page_not_found(e):
 #   return render_template('404.html'), 404

#@app.route("/")
#def index():
    #return render_template('index.html')
    
@app.route('/')
def index():
    return render_template('index.html')
    
def add():
    add=True
    return redirect(url_for('index'))


@app.route('/search.html')
def search():

#get the input and make it a list
    
    data=request.args.get('q', None)
    if not data:
    	flash("Please enter a valid username!")
    	return redirect(url_for('index'))
    y=request.args.get('Location', None)
    datalist=data.split(',')
    
#get the locations that the usernames have been    
    
    loc=[]
    for i in datalist:
        loc+=getlocations.getlocation(i)
        
 #get the final list of the restaurant suggestions       
    
    final=restsuggestions.giverest(loc,y)
    if final:
        if len(final)>=3:
            final=final[:3]
    
 #get all the photos of the restaurant   
    
        fotos={}
        numfotos={}
        for res in final:
            fotos[res]=takefoto.foto(res,y)
            numfotos[res]=len(fotos[res])

#sort the restaurants wrt the number of the photos    
    
        final=sorted(numfotos, key=numfotos.__getitem__, reverse=True)
    
#get geolocations of the restaurants    
        latlong=[]
        for res in final:
            latlong.append(restsuggestions.latlong(res,y))

#make rank dictionary   
        dicrank={}
        for res in final:
            sql1="""SELECT rank FROM %s WHERE name="%s" """ % (city[y],res)
            a=psql.frame_query(sql1, con=con)
            b=a.values.tolist()
            dicrank[res]=float(b[0][0])
    
 #get the category of the restaurant   
        sql1="""SELECT category FROM %s WHERE name="%s" """ % (city[y],final[0])
        a=psql.frame_query(sql1, con=con)
        b=a.values.tolist()
        categ=catfunc(b[0][0])
    
  
  #get the address of the restaurant  
        dicadd={}         
        for res in final:
            sql1="""SELECT address FROM %s WHERE name="%s" """ % (city[y],res) 
            a=psql.frame_query(sql1, con=con) 
            b=a.values.tolist()
            if b[0]:
                dicadd[res]=b[0][0]
            else:
                dicadd[res]='There is no address.'
                
    else:
        flash("Sorry! You can use this app only if you have previously posted a photo/video from a restaurant in the Bay Area.  If you have done so, please change the search location and try again.")
    	return redirect(url_for('index'))           
    
    return render_template('search.html', data=data, final=final, y=y, latlong=latlong, fotos=fotos, dicrank=dicrank, categ=categ, dicadd=dicadd)





if __name__=="__main__":
   port=int(os.environ.get("PORT", 5000))
   app.run(host='0.0.0.0', port=port, debug=True)