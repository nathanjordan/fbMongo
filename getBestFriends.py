'''
Created on May 7, 2012

@author: njordan
'''
from pymongo.code import Code
from pymongo import Connection
import fbMongo
import pymongo

funcMap = Code("function map() {  emit( this.userID , 1 ); }")
    
funcReduce = Code("function reduce( key , values ) { var result = 0; values.forEach(function(value) {" +
            "result += value;" +
            "});" +
            "return result;" +
            "}" )

accessToken = raw_input("Enter AuthID: ")

connection = Connection("localhost", 27017).facebook

userAggregateCollection = connection.bestFriendsCounter

music = fbMongo.getFacebookObject(connection, accessToken, "me", "music")

userid = fbMongo.getFacebookObject(connection, accessToken, "me", "")["id"]

for x in music:
    # { "artistID" : x["artistID"] }
    results = connection.musicCollection.find( { "artistID" : x["id"] } )
    
    for y in results:
        
        userAggregateCollection.insert( { "userID" : y["userID"] } )
        
userAggregateCollection.map_reduce( funcMap , funcReduce , "bestFriendsResult" )

ownLikes = 0

for x in connection.bestFriendsResult.find().sort("value",pymongo.DESCENDING).limit(25):
    
    user = fbMongo.getFacebookObject(connection, accessToken, x["_id"], "")
    
    if x["_id"] == userid:
        
        ownLikes = x["value"]
        
        continue
    
    print user["name"] + " " + str(x["value"] / ownLikes) + "%"
    
connection.bestFriendsResult.drop()

