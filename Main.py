'''
Created on Apr 30, 2012

@author: njordan
'''

from pymongo import Connection
from pymongo.code import Code
import json
import urllib2
import sys

#################################################################################################################

def getFacebookObject( accessToken , objectID , query ):
    
    if query != "":
        
        response = urllib2.urlopen("https://graph.facebook.com/" + objectID + "/" + query + "/?access_token=" + accessToken )
    
    else:
        
        response = urllib2.urlopen("https://graph.facebook.com/" + objectID + "/?access_token=" + accessToken )
    
    response = json.loads( response.read() )
    
    try:
        
        return response["data"]
    
    except Exception:
        
        return response
    
#################################################################################################################

accessToken = "AAACEdEose0cBAH5rGc8xYPva5tEsVVZAZCh9hOvGIiGuMoy9neIldHBTTKisELw3MFdtZBc37bZCt3auSLZC8WagG4igKxeUlwWneCajqygZDZD"

userID = "820047987"

#connect to mongodb
connection = Connection('localhost', 27017)

db = connection.facebook

musicCollection = db.music

musicCollection.drop()

#myMusic = getFacebookObject( accessToken , userID, "music" )

for x in myMusic:
    
    musicCollection.insert( { "id" : x["id"] , "name" : x["name"] } )
    
    info = getFacebookObject( accessToken , x["id"], "" )
    
    musicCollection.insert( { "id" : info["id"] , "name" : info["name"] } )
    
friends = getFacebookObject( accessToken , userID, "friends" )

for x in friends:
    
    print "getting music for " + x["name"]
    
    music = getFacebookObject( accessToken , x["id"], "music" )
    
    for y in music:
        #if you use x here instead of y, you actually
        #computer how many artists you have in common with a friend, cool!!!!!
        musicCollection.insert( { "id" : y["id"] , "name" : y["name"] , "userID" : x["id"] } )
        
#map reduce it
funcMap = Code("function map() {  emit( this.id , 1 ); }")

funcMapUsers = Code("function map() {  emit( this.userID , 1 ); }")

funcReduce = Code("function reduce( key , values ) { var result = 0; values.forEach(function(value) {" +
            "result += value;" +
            "});" +
            "return result;" +
            "}" )

db.music.map_reduce( funcMap , funcReduce , "musicResult" )

top25 = db.musicResult.find().sort( "value" , -1 ).limit(25)

print "Top 25 artists in from your friends: "

for x in top25:
    
    info = getFacebookObject( accessToken , x["_id"], "" )
    
    print info["name"] + " : " + str(x["value"])
    
db.music.map_reduce( funcMapUsers , funcReduce , "userResult" )

top25 = db.userResult.find().sort( "value" , -1 ).limit(25)

print "Top 25 music friends: "

for x in top25:
    
    info = getFacebookObject( accessToken , x["_id"], "" )
    
    print info["name"] + " : " + str(x["value"])






























