import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class RewardsHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.database = MongoClient("mongodb", 27017)["Rewards"]

    @coroutine
    def get(self):
        rewards = list(self.database.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
