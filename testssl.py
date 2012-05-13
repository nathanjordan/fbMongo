import tornado.ioloop
import tornado.web
import urllib2
import fbMongo
import time
import os
from pymongo import Connection
from tornado.httpserver import HTTPServer

APPID = "362735243774306"
APPSECRET = "9e283992e0ba5892ddf42ad548176472"
REDIRECT_URI = "https://mrnapalm32.dyndns.org:9999/access"
ACCESSTOKEN_URI = "https://mrnapalm32.dyndns.org:9999/token"
USER_SCOPE = "user_likes,user_religion_politics,user_relationships,user_hometown,user_location,user_birthday"
FRIEND_SCOPE = ",friends_likes,friends_religion_politics,friends_relationships,friends_hometown,friends_location,friends_birthday"

SCOPE = USER_SCOPE + FRIEND_SCOPE

connection = Connection("localhost", 27017).facebook

class InitialHandler(tornado.web.RequestHandler):
    def get(self):
        url = "https://www.facebook.com/dialog/oauth?client_id=" + APPID + "&redirect_uri=" + REDIRECT_URI + "&scope=" + SCOPE + "&state=fff"
        self.redirect(url)
        #code = self.get_argument("code")
        #self.write("feck")
        #self.write(code)
        #r = "https://graph.facebook.com/oauth/access_token?client_id=" + APPID + "&redirect_uri=" + REDIRECT_URI + "&client_secret=" + APPSECRET + "&code=" + code
        #r = urllib2.urlopen(r)
        #self.write(r)
    
    def post(self):
        url = "https://www.facebook.com/dialog/oauth?client_id=" + APPID + "&redirect_uri=" + REDIRECT_URI + "&scope=user_likes,friends_likes&state=fff"
        self.redirect(url)
        #code = self.get_argument("code")
        #self.write("feck")
        #self.write(code)
        #r = "https://graph.facebook.com/oauth/access_token?client_id=" + APPID + "&redirect_uri=" + REDIRECT_URI + "&client_secret=" + APPSECRET + "&code=" + code
        #r = urllib2.urlopen(r)
        #self.write(r)
        
class UserCodeHandler(tornado.web.RequestHandler):
    def get(self):
        code = self.get_argument("code")
        r = "https://graph.facebook.com/oauth/access_token?client_id=" + APPID + "&redirect_uri=" + REDIRECT_URI + "&client_secret=" + APPSECRET + "&code=" + code
        r = urllib2.urlopen(r)
        url = ACCESSTOKEN_URI + "?"  + r.read()
        self.redirect(url)
        #self.write("done")

class TokenHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument("access_token")
        expires = self.get_argument("expires")
        userID = fbMongo.getFacebookObject( token , "me", "")["id"]
        expireTime = time.time() + int(expires)
        connection.accessTokens.remove( { "userId" : userID } )
        connection.accessTokens.insert( { "userId" : userID , "token" : token , "expires" : expireTime } )
        self.write("<h5>Thanks!</h5>")
        
application = tornado.web.Application([
    (r"/", InitialHandler),
    (r"/access", UserCodeHandler),
    (r"/token", TokenHandler),
])

http_server = HTTPServer(application,
    ssl_options={
    "certfile": os.path.join("", "mrnapalm32.dyndns.org.crt"),
    "keyfile": os.path.join("", "keynew.key"),
    }) 

if __name__ == "__main__":
    http_server.listen(9999)
    tornado.ioloop.IOLoop.instance().start()
