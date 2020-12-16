# written by Edward Barbezat 12/16/20
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class UserRewards(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        email = self.get_argument('email')
        client = MongoClient("mongodb", 27017)
        db = client["Users"]
        user = db.users.find_one({"email": email})
        self.write(str(user))
