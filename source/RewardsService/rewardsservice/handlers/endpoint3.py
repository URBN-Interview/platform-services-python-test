import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class Endpoint3(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        users = list(db.users.find({}, {"_id": 0}))

        self.write(json.dumps(users))