'''
Created on May 13, 2012

@author: njordan
'''

from pymongo.code import Code
from pymongo import Connection
import fbMongo
import pymongo
import time

db = Connection("localhost", 27017).facebook

db.likesCounts.drop()

accessToken = "AAACEdEose0cBAJYjYIsXCrSs3C18Qeb9Nyh4lKA8hUO4S9EY9xRcgZBQDmVkG8iy0CZCZAuJG5O30ctSHfj7OO6OhGz2C1RrNNrdVuPtQZDZD"

#get the top likes
funcMap = Code("function map() {  emit( this.id , 1 ); }")
    
funcReduce = Code("function reduce( key , values ) { var result = 0; values.forEach(function(value) {" +
            "result += value;" +
            "});" +
            "return result;" +
            "}" )

filters = { "$and" : [] }

filters["$and"].append( { "category" : { "$ne" : "Movie" } })
filters["$and"].append( { "category" : { "$ne" : "Musician/band"} })
filters["$and"].append( { "category" : { "$ne" : "Tv show" } })

print "-=-=-=-=-=- Likes -=-=-=-=-=-=-"

db.likes.map_reduce( funcMap , funcReduce , "likesCounts" , query = filters )

results = db.likesCounts.find().sort( "value" , pymongo.DESCENDING ).limit(50)

for x in results:
    
    value = fbMongo.getFacebookObject(accessToken, x["_id"], "" )
    
    print value["name"]
    
    time.sleep(0.2)
    
print "-=-=-=-=-=- Music -=-=-=-=-=-=-"

db.likesCounts.drop()

db.likes.map_reduce( funcMap , funcReduce , "likesCounts" , query = { "category" : "Musician/band" } )

results = db.likesCounts.find().sort( "value" , pymongo.DESCENDING ).limit(50)

for x in results:
    
    value = fbMongo.getFacebookObject(accessToken, x["_id"], "" )
    
    print value["name"]
    
    time.sleep(0.2)

print "-=-=-=-=-=- Movies -=-=-=-=-=-=-"

db.likesCounts.drop()

db.likes.map_reduce( funcMap , funcReduce , "likesCounts" , query = { "category" : "Movie" } )

results = db.likesCounts.find().sort( "value" , pymongo.DESCENDING ).limit(50)

for x in results:
    
    value = fbMongo.getFacebookObject(accessToken, x["_id"], "" )
    
    print value["name"]
    
    time.sleep(0.2)

print "-=-=-=-=-=- Relationships -=-=-=-=-=-=-"


funcMap = Code("function map() {  emit( this.relationship_status , 1 ); }")
    
funcReduce = Code("function reduce( key , values ) { var result = 0; values.forEach(function(value) {" +
            "result += value;" +
            "});" +
            "return result;" +
            "}" )

results = db.likes.map_reduce( funcMap , funcReduce , "results" )

for x in results:
    
    print x["_id"] + " " + x["value"]










    