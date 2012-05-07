'''
Created on May 6, 2012

@author: njordan
'''

from pymongo import Connection
import fbMongo

accessToken = "AAACEdEose0cBAKQZClNkYzzDKKBM3wlrvG884TBogtgZBaQQRzkVmqjGtqLaDbOqH5MSaoZAZBAZAjeL64eSCO3vXZCFzUDIkRxvP8ZAqdSZCwZDZD"

userID = "820047987"

#connect to mongodb
connection = Connection("localhost", 27017).facebook

fbMongo.insertFriendsMusic( connection, accessToken, userID, "musicCollection" )