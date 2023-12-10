import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

CLIENT = MongoClient("mongodb", 27017)

class UsersHandler(tornado.web.RequestHandler):
    #GET method for finding single user data or all users data
    @coroutine
    def get(self):
        db = CLIENT["Rewards"]
        users = db["users"]
        email = self.get_query_argument("email", None)
        if(email): 
            found_user = users.find_one({"email_address": email})
            self.write(json.dumps(found_user))
        else:
            found_users = list(users.find())
            self.write(json.dumps(found_users))