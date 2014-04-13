import urllib
import json
import requests

#get the user id from the username

def getuserid(x):

    req=requests.get("https://api.instagram.com/v1/users/search?q="+x+"&access_token=232690335.f8c47bd.caf347ce037a42c29805a4f389aaf788")
    js=req.json()
    d=dict(js)
    d=d['data']
    d=d[-1]
    return str(d['id'])


#get the locations that the username has been

def getlocation(x):
    id = getuserid(x)  
    req=requests.get("https://api.instagram.com/v1/users/"+id+"/media/recent/?access_token=232690335.f8c47bd.caf347ce037a42c29805a4f389aaf788")
    js = req.json()
    d = dict(js)
    alist=d['data']
    

     
    locations=[]

    for i in range(len(alist)):
        adic=alist[i]
        dicloc=adic['location']
        if type(dicloc) is dict:
            if 'name' in dicloc.keys():
                locations.append(dicloc['name'])
           
    return locations
     
    
    
