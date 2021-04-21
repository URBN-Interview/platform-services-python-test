import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

# accept customer email and order total
class Endpoint1(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        # get all rewards
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
        