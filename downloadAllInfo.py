'''
Created on May 12, 2012

@author: njordan
'''

from pymongo import Connection
import fbMongo

print "This script will insert all your friends stuff into mongo collections"

#connect to mongodb
connection = Connection("localhost", 27017).facebook

connection.likes.drop()

connection.athletes.drop()

connection.friends.drop()

connection.sports.drop()

connection.teams.drop()

#for every user whos authenticated, get their ID's
for x in connection.accessTokens.find():
    
    userID = x["userId"]
    
    accessToken = x["token"]
    
    #get all their friends
    friends = fbMongo.getFacebookObject(accessToken, "me", "friends")
    
    #for every friend they have
    for y in friends:
        
        #get their ID
        friendId = y["id"]
        
        #get their music
        likes = fbMongo.getFacebookObject(accessToken, friendId , "likes")
        
        try:
            
            #insert their likes
            for z in likes:
                
                likeId = z["id"]
                
                likeName = z["name"]
                
                likeCategory = z["category"]
                
                connection.likes.insert( { "id" : likeId , "name" : likeName , "category" : likeCategory , "userId" : friendId } )
                    
        except KeyError:
            None
            
        friend = fbMongo.getFacebookObject(accessToken, friendId , "")
        
        try:
            for z in friend["sports"]:
                
                z["userId"] = friendId
                
                connection.sports.insert( z )
                
        except KeyError:
            None
         
        try:
            for z in friend["favorite_teams"]:
                
                z["userId"] = friendId
                
                connection.teams.insert( z )
                    
        except KeyError:
            None
        
        try:
            for z in friend["favorite_athletes"]:
                
                z["userId"] = friendId
                
                connection.athletes.insert( z )
                    
        except KeyError:
            None
            
        data = { "id" : friendId }
        
        #gender
        try:
            data["gender"] = friend["gender"]
        except KeyError:
            None
            
        #interested in
        try:
            data["interested_in"] = friend["interested_in"] 
        except KeyError:
            None
            
        #interested in
        try:
            data["birthday"] = friend["birthday"]
        except KeyError:
            None
            
        #interested in
        try:
            data["political"] = friend["political"]
        except KeyError:
            None
            
        #location
        try:
            data["location"] = friend["location"]["name"]
        except KeyError:
            None
            
        #hometown
        try:
            data["hometown"] = friend["hometown"]["name"]
        except KeyError:
            None
            
        #relationship status
        try:
            data["relationship_status"] = friend["relationship_status"]
        except KeyError:
            None
        
        connection.friends.insert( data )
            
        
        
            
        
    