'''
Created on May 7, 2012

@author: njordan
'''

from pymongo import Connection
import fbMongo

print "This script will insert all your friends music into a mongo collection"

accessToken = raw_input("Access Token: ")

#connect to mongodb
connection = Connection("localhost", 27017).facebook

userID = fbMongo.getFacebookObject(connection, accessToken, "me", "")["id"]

print "Working..."

fbMongo.insertFriendsMovies( connection, accessToken, userID, "movieCollection" )