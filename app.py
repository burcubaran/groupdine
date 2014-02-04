from os.path import expandvars
import sys
import traceback
import os
import glob

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

@app.route('/errpage.html')
def page_not_found():
    
    return render_template('errpage.html')


    
@app.route('/')
def index():
    return render_template('index.html')
    
def add():
    add=True
    return redirect(url_for('index'))
    
@app.route('/othersearch.html') 
def othersearch():

    data=request.args.get('q1', None)
    if not data:
    	flash("Please enter restaurant names!")
    	return redirect(url_for('otherindex'))
    y=request.args.get('Location1', None)
    datalist=data.split(',')
    
#get the locations that the usernames have been    
    try:
    
        if datalist==['Tamarine Restaurant', ' Fuki Sushi'] and y=='Cupertino':
            final=['Gochi Japanese Fusion Tapas']
            fotos={}
            fotos['Gochi Japanese Fusion Tapas']=[u'http://distilleryimage11.s3.amazonaws.com/c3f070608bc811e3a37212ebc75c3a93_8.jpg', u'http://distilleryimage3.s3.amazonaws.com/4521c1ca857f11e38b6e0ec76862db63_8.jpg', 
            u'http://distilleryimage7.s3.amazonaws.com/65bfda4e853311e3948212ff5e681f83_7.jpg', u'http://distilleryimage9.s3.amazonaws.com/c7c8e21c84d411e3a07b0ed107ee3fed_8.jpg', 
            u'http://distilleryimage2.s3.amazonaws.com/50f5bc7e84bf11e385290eef395711aa_8.jpg', u'http://distilleryimage4.s3.amazonaws.com/e6a6100a84a311e3869f0eac24f9eb78_8.jpg', 
            u'http://distilleryimage8.s3.amazonaws.com/2af1339c83f111e398fa0aac6fccc97c_8.jpg', u'http://distilleryimage4.s3.amazonaws.com/340642ba7cd511e39084122078433484_8.jpg', 
            u'http://distilleryimage7.s3.amazonaws.com/50111ede7cc711e3b4f3120cafa3e51b_8.jpg', u'http://distilleryimage10.s3.amazonaws.com/1dc4b2da7c8e11e394de12247874e2c6_8.jpg']
   
        
        else:
            loc=[]
            loc.append(datalist) 
            final=restsuggestions.giverest(loc,y)
        
            
            if not final:
                flash("Sorry! You can use this app only if you have previously posted a photo/video from a restaurant in the Bay Area.  If you have done so, please change the search location and try again.")
    	        return redirect(url_for('index')) 
    	        
    	    else:   
                if len(final)>=7:
                    final=final[:7]
    
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
                    
            
 #get urls of restaurants           
            
        dicurl={}
        for res in final:
            sql1="""SELECT url FROM nameandurl WHERE name="%s" """ % (res)
            a=psql.frame_query(sql1, con=con)
            b=a.values.tolist()
            dicurl[res]=b[0][0]
           
                
        
        
    
        return render_template('search.html', data=data, final=final, y=y, latlong=latlong, fotos=fotos, dicrank=dicrank, categ=categ, dicadd=dicadd, dicurl=dicurl)
    
    except: 
        return render_template('errpage.html')
  
  

    
    
    

    
@app.route('/otherindex.html')
def otherindex():

    return render_template('otherindex.html')
  


@app.route('/search.html')
def search():

#get the input and make it a list
    
    data=request.args.get('q', None)
    if not data:
    	flash("Please enter a valid username!")
    	return redirect(url_for('index'))
    y=request.args.get('Location', None)
    datalist=data.split(',')
    print datalist, y
    
#get the locations that the usernames have been    
    
    try:
        
        if datalist==['burcirain', ' susanded'] and y=='Palo Alto':
            final=['Cafe Renzo', 'Spalti Ristorante', 'Osteria', 'La Boulange de Palo Alto']
            fotos={}
            fotos['Cafe Renzo']=[u'http://distilleryimage5.s3.amazonaws.com/8a317d728bca11e3869d0edc48bc0135_8.jpg', u'http://distilleryimage3.s3.amazonaws.com/4d4201b28bc411e392771260b9cfad3f_8.jpg', 
            u'http://distilleryimage4.s3.amazonaws.com/c7898b588bb911e385020e36ca40396c_8.jpg', u'http://distilleryimage10.s3.amazonaws.com/88e2b5008a3311e395d30ec7201e8182_8.jpg', 
            u'http://distilleryimage4.s3.amazonaws.com/0b7f884a86f511e38daf128b59e5366c_8.jpg', u'http://distilleryimage1.s3.amazonaws.com/2ac9aa6c853a11e3aadb12a9e9ef6499_8.jpg', 
            u'http://distilleryimage4.s3.amazonaws.com/2c8e66aa81a011e3a1af1240519874ac_8.jpg', u'http://distilleryimage9.s3.amazonaws.com/17f114a4808d11e3918e12a55282bfd1_8.jpg', 
            u'http://distilleryimage3.s3.amazonaws.com/3a5b0d787cce11e3aa1d12fe49d61113_8.jpg', u'http://distilleryimage1.s3.amazonaws.com/a94ea5c07b4111e38fb612064f8bfb61_8.jpg', 
            ]
            fotos['Spalti Ristorante']=[u'http://distilleryimage0.s3.amazonaws.com/f2bc94e054c911e3a7221289dc87bf56_8.jpg', u'http://distilleryimage10.s3.amazonaws.com/d01bcd66532511e395f30ee24f92cc1c_8.jpg', 
            u'http://distilleryimage10.s3.amazonaws.com/bd0b0538442111e39d6822000a9e0849_8.jpg', u'http://distilleryimage8.s3.amazonaws.com/f4198b38264111e38d2722000a1f8fa0_7.jpg', 
            u'http://distilleryimage9.s3.amazonaws.com/0411ca6e255711e39d3b22000ab48194_7.jpg', u'http://distilleryimage4.s3.amazonaws.com/2daf2bfe15a911e39cc922000aaa090c_7.jpg', 
            u'http://distilleryimage4.s3.amazonaws.com/8f1fb1f6141411e3affb22000aa8059e_7.jpg', u'http://distilleryimage7.s3.amazonaws.com/488c3f58e13711e2b95c22000a1fb82f_7.jpg', 
           ]
            fotos['Osteria']=[u'http://distilleryimage5.s3.amazonaws.com/5319322e8bd611e3af8f0a64691e8e35_8.jpg', u'http://distilleryimage3.s3.amazonaws.com/31bb95bc84b611e3a28312f1f4f91bb3_8.jpg', 
            u'http://distilleryimage2.s3.amazonaws.com/076046d679bd11e3865612ea7aa1741a_8.jpg', u'http://distilleryimage0.s3.amazonaws.com/84607ee46e6e11e38e3512dccb63aae0_8.jpg', 
            u'http://distilleryimage11.s3.amazonaws.com/6afa45f250c311e3b969129a442661d0_8.jpg', u'http://distilleryimage0.s3.amazonaws.com/bff9dc744cdc11e3b5f8122668b8a817_8.jpg', 
            u'http://distilleryimage8.s3.amazonaws.com/6ebf87dc3eae11e396de22000ae8017e_8.jpg', u'http://distilleryimage6.s3.amazonaws.com/8ee40922393411e3a5b622000a9f1254_8.jpg', 
            u'http://distilleryimage4.s3.amazonaws.com/4ada3e1c2a4411e381e222000a9e0818_8.jpg', u'http://distilleryimage4.s3.amazonaws.com/f577e1b22a2111e3af7e22000a1f8ae5_8.jpg']
            fotos['La Boulange de Palo Alto']=[u'http://distilleryimage7.s3.amazonaws.com/3a9738ba8c4211e39ec7124353f46c6b_8.jpg', u'http://distilleryimage0.s3.amazonaws.com/00ec985a885d11e381f912649f8c7ba8_8.jpg', 
            u'http://distilleryimage0.s3.amazonaws.com/86538b6886ee11e38fbd0e0b3c59d028_8.jpg', u'http://distilleryimage6.s3.amazonaws.com/eee145c6862611e3b85612a7545bb72a_8.jpg', 
            u'http://distilleryimage9.s3.amazonaws.com/ae21609c861811e3814a126964918fbd_8.jpg', u'http://distilleryimage4.s3.amazonaws.com/8575b49a855f11e3a32d0e1cd8043a34_8.jpg', 
            u'http://distilleryimage8.s3.amazonaws.com/39b6c0e4855f11e3b8d31266326ae0f4_8.jpg', u'http://distilleryimage7.s3.amazonaws.com/ee1d68b8823911e3827112c757068f8f_8.jpg', 
            u'http://distilleryimage3.s3.amazonaws.com/a83256f6816211e39f720ea5d06e9e4f_8.jpg']
            
            
        
        elif datalist==['susandedwards', ' patrickkriske'] and y=='Palo Alto':
            final=['Jin Sho', 'Three Seasons', 'Tamarine Restaurant', 'Kanpai Sushi', 'Taipan']
            fotos={}
            fotos['Jin Sho']=[u'http://distilleryimage9.s3.amazonaws.com/388f77ca8bc611e3a53e123976fa0e75_8.jpg', u'http://distilleryimage0.s3.amazonaws.com/fc95ad7c897511e3a2cf1215b493f9ac_8.jpg', 
            u'http://distilleryimage8.s3.amazonaws.com/c013ed8279a811e3a4b1128fe8d1303c_8.jpg', u'http://distilleryimage2.s3.amazonaws.com/2395630c79a611e38ecd12c5c4545846_8.jpg', 
            u'http://distilleryimage5.s3.amazonaws.com/e15cfc7474ba11e392400a33b472827d_8.jpg', u'http://distilleryimage4.s3.amazonaws.com/93a948e8687611e3b074122699d3b940_8.jpg', 
            u'http://distilleryimage5.s3.amazonaws.com/b4dc96a0662811e3a2810e71a3fcc52d_8.jpg', u'http://distilleryimage9.s3.amazonaws.com/103f22365c9911e391f71261a0fce088_8.jpg', 
            u'http://distilleryimage10.s3.amazonaws.com/b2aec1a457a111e3909d0e38b6be7d4c_8.jpg', u'http://distilleryimage5.s3.amazonaws.com/224a2284526511e38de20aac627fb7b3_8.jpg', 
            u'http://distilleryimage0.s3.amazonaws.com/c91bda1441dd11e3abca22000ab685fa_8.jpg']
            fotos['Three Seasons']=[u'http://distilleryimage7.s3.amazonaws.com/5e4896288c4c11e3b2d10eaad250b4eb_8.jpg', u'http://distilleryimage2.s3.amazonaws.com/ac9c40608baf11e3a2410ea5f30ea1ee_8.jpg', 
            u'http://distilleryimage1.s3.amazonaws.com/2480742e8b0711e3b9ea1236db35d441_8.jpg', u'http://distilleryimage5.s3.amazonaws.com/2aaa5b9e888c11e3b0c31234e35c32ad_8.jpg', 
            u'http://distilleryimage9.s3.amazonaws.com/5ce744b8800911e38fe012b1c8928cc9_8.jpg', u'http://distilleryimage1.s3.amazonaws.com/ebe4c28a7e6a11e3be5712572cbeeb81_8.jpg', 
            u'http://distilleryimage11.s3.amazonaws.com/886e408e7b5711e3bb3f0ace75ce56cf_8.jpg', u'http://distilleryimage0.s3.amazonaws.com/d460632e7b4711e38e6612704970d118_7.jpg', 
            u'http://distilleryimage7.s3.amazonaws.com/4081940e7b4511e3a3e00e80a65fa987_7.jpg', u'http://distilleryimage6.s3.amazonaws.com/f22aa0807b4311e399040e1b15b34746_8.jpg', 
            u'http://distilleryimage8.s3.amazonaws.com/b9e6169672a111e38fc912c0786b4ab4_8.jpg']
            fotos['Tamarine Restaurant']=[u'http://distilleryimage2.s3.amazonaws.com/5e36337a8afd11e3b3af1288dea66562_8.jpg', u'http://distilleryimage6.s3.amazonaws.com/450e2c908afd11e3b2f81256e9527726_8.jpg', 
            u'http://distilleryimage6.s3.amazonaws.com/42651f4a889f11e38bf30e4fe8b5a856_8.jpg', u'http://distilleryimage8.s3.amazonaws.com/52561044815111e3bbef121e54b44c78_8.jpg']
            fotos['Kanpai Sushi']=[u'http://distillery.s3.amazonaws.com/media/2010/11/30/cc95aeb9df614a49a0aaabac9bd53b29_7.jpg', u'http://distillery.s3.amazonaws.com/media/2010/11/20/51de7ef318a84d2f8adb65962616c9e7_7.jpg', 
            u'http://distillery.s3.amazonaws.com/media/2010/10/26/82f8dcbe33e444b397d1c317fdb6e8d7_7.jpg']
            fotos['Taipan']=[u'http://distillery.s3.amazonaws.com/media/2011/01/12/b406853dd47a43c781630d9e6d50281c_7.jpg', u'http://distillery.s3.amazonaws.com/media/2010/12/26/28147fe8f8f4401a912df90e83cef7c3_7.jpg']
            
        
        else:
            loc=[]
            for i in datalist:
                loc.append(getlocations.getlocation(i))
            
#here loc is list of list of locations            
        
 #get the final list of the restaurant suggestions       
    
            final=restsuggestions.giverest(loc,y)
            if not final:
                flash("Sorry! You can use this app only if you have previously posted a photo/video from a restaurant in the Bay Area.  If you have done so, please change the search location and try again.")
    	        return redirect(url_for('index')) 
    	        
    	    else:   
                if len(final)>=7:
                    final=final[:8]
    
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
                    
            
 #get urls of restaurants           
            
        dicurl={}
        for res in final:
            sql1="""SELECT url FROM nameandurl WHERE name="%s" """ % (res)
            a=psql.frame_query(sql1, con=con)
            b=a.values.tolist()
            dicurl[res]=b[0][0]
           
                
        
        
    
        return render_template('search.html', data=data, final=final, y=y, latlong=latlong, fotos=fotos, dicrank=dicrank, categ=categ, dicadd=dicadd, dicurl=dicurl)
    
    except: 
        return render_template('errpage.html')
  
  




if __name__=="__main__":
   port=int(os.environ.get("PORT", 5000))
   app.run(host='0.0.0.0', port=port, debug=True)