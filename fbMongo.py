'''
Created on Apr 30, 2012

@author: njordan
'''

from pymongo.code import Code
import json
import urllib2

#################################################################################################################

def getFacebookObject( connection, accessToken , objectID , query ):
    
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

def insertMusicForUser( connection, accessToken , userID , collectionName ):
    
    music = getFacebookObject( connection , accessToken , userID , "music" )
    
    collection = connection[ collectionName ]
    
    for y in music:
        
        collection.insert( { "artistID" : y["id"] , "artistName" : y["name"] , "userID" : userID } )

#################################################################################################################

def insertFriendsMusic( connection , accessToken,  userID , collectionName ):
    
    friends = getFacebookObject( connection , accessToken , userID , "friends" )
    
    for x in friends:
        
        insertMusicForUser( connection , accessToken , x["id"] , collectionName )
    
#################################################################################################################

def getTopArtists( connection , collectionName , resultCollection ):
    
    collection = connection[ collectionName ]
    
    #map reduce it
    funcMap = Code("function map() {  emit( this.artistName , 1 ); }")
    
    funcReduce = Code("function reduce( key , values ) { var result = 0; values.forEach(function(value) {" +
                "result += value;" +
                "});" +
                "return result;" +
                "}" )
    
    collection.map_reduce( funcMap , funcReduce , resultCollection )

#################################################################################################################
































