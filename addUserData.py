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

likes = db.likes2.find()

for x in likes:
    
    user = db.friends.find_one({ "id" : x["userId"]} )
    
    #gender
    try:
        x["gender"] = user["gender"]
    except KeyError:
        None
        
    #interested in
    try:
        x["political"] = user["political"]
    except KeyError:
        None
        
    #relationship status
    try:
        x["relationship_status"] = user["relationship_status"]
    except KeyError:
        None
        
    db.likes2.save(x)