'''
Created on May 7, 2012

@author: njordan
'''

from pymongo import Connection
import fbMongo

print "This script will insert all your friends stuff into mongo collections"

accessToken = raw_input("Access Token: ")

#connect to mongodb
connection = Connection("localhost", 27017).facebook

userID = fbMongo.getFacebookObject(connection, accessToken, "me", "")["id"]

print "Inserting Friends Music..."

fbMongo.insertFriendsMusic( connection, accessToken, userID, "musicCollection" )

print "Inserting Friends Movies..."

fbMongo.insertFriendsMovies( connection, accessToken, userID, "movieCollection" )

print "Inserting Friends Likes..."

fbMongo.insertFriendsLikes( connection, accessToken, userID, "likeCollection" )

print "Finished! Goodbye"