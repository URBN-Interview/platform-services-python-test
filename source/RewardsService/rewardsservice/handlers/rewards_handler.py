import json

import tornado.web
from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsHandler(tornado.web.RequestHandler):

    client = MongoClient("mongodb", 27017)
    db = client["Rewards"]

    @coroutine
    def get(self):
        rewards = list(self.db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
