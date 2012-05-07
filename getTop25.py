'''
Created on May 6, 2012

@author: njordan
'''

import fbMongo
from pymongo import Connection
import pymongo

#connect to mongodb
connection = Connection("localhost", 27017).facebook

fbMongo.getTopArtists(connection, "musicCollection" , "top25" )

for x in connection.top25.find().sort("value",pymongo.DESCENDING).limit(25):
    
    print x["_id"] + " " + str(x["value"])
    
connection.top25.drop()