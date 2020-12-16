# written by Edward Barbezat 12/16/20
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class AllUserRewards(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Users"]
        users = list(db.users.find({}))
        self.write(str(users))
