'''
Created on Apr 30, 2012

@author: njordan
'''

from pymongo.code import Code
import json
import urllib2
from urllib2 import HTTPError
import time

#################################################################################################################

def getFacebookObject( accessToken , objectID , query ):
    
    errorCount = 0
    
    response = ""
    
    while errorCount < 4:
        
        try:
            
            if query != "":
                
                response = urllib2.urlopen("https://graph.facebook.com/" + objectID + "/" + query + "/?access_token=" + accessToken )
            
            else:
                
                response = urllib2.urlopen("https://graph.facebook.com/" + objectID + "/?access_token=" + accessToken )
                
            break
        
        except HTTPError:
            
            errorCount += 1
            
            time.sleep(0.5)
            
    if errorCount == 4:
        
        print "Error occured reading object " + objectID
        
        return
        
    else:
    
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

def insertMoviesForUser( connection, accessToken , userID , collectionName ):
    
    movies = getFacebookObject( connection , accessToken , userID , "movies" )
    
    collection = connection[ collectionName ]
    
    for y in movies:
        
        collection.insert( { "movieID" : y["id"] , "movieName" : y["name"] , "userID" : userID } )

#################################################################################################################

def insertFriendsMovies( connection , accessToken,  userID , collectionName ):
    
    friends = getFacebookObject( connection , accessToken , userID , "friends" )
    
    for x in friends:
        
        insertMoviesForUser( connection , accessToken , x["id"] , collectionName )

##########################################################################################

def getTopMovies( connection , collectionName , resultCollection ):
    
    collection = connection[ collectionName ]
    
    #map reduce it
    funcMap = Code("function map() {  emit( this.userId + this.id , 1 ); }")
    
    funcReduce = Code("function reduce( key , values ) { var result = 0; values.forEach(function(value) {" +
                "result += value;" +
                "});" +
                "return result;" +
                "}" )
    
    collection.map_reduce( funcMap , funcReduce , resultCollection )


def insertLikesForUser( connection, accessToken , userID , collectionName ):
    
    movies = getFacebookObject( connection , accessToken , userID , "likes" )
    
    collection = connection[ collectionName ]
    
    for y in movies:
        
        collection.insert( { "pageID" : y["id"] , "pageName" : y["name"] , "userID" : userID } )

#################################################################################################################

def insertFriendsLikes( connection , accessToken,  userID , collectionName ):
    
    friends = getFacebookObject( connection , accessToken , userID , "friends" )
    
    for x in friends:
        
        insertLikesForUser( connection , accessToken , x["id"] , collectionName )

##########################################################################################

def getTopLikes( connection , collectionName , resultCollection ):
    
    collection = connection[ collectionName ]
    
    #map reduce it
    funcMap = Code("function map() {  emit( this.pageName , 1 ); }")
    
    funcReduce = Code("function reduce( key , values ) { var result = 0; values.forEach(function(value) {" +
                "result += value;" +
                "});" +
                "return result;" +
                "}" )
    
    collection.map_reduce( funcMap , funcReduce , resultCollection )






















