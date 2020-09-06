import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))

class CustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))

    def findRewardTier(self, totalSpent):
        if totalSpent >= 1000:
            return "J"
        elif totalSpent >= 800 and totalSpent < 900:
            return "I"
        elif totalSpent >= 700 and totalSpent < 800:
            return "H"
        elif totalSpent >= 600 and totalSpent < 700:
            return "G"
        elif totalSpent >= 500 and totalSpent < 600:
            return "F"
        elif totalSpent >= 400 and totalSpent < 500:
            return "E"
        elif totalSpent >= 300 and totalSpent < 400:
            return "D"
        elif totalSpent >= 200 and totalSpent < 300:
            return "C"
        elif totalSpent >= 100 and totalSpent < 200:
            return "B"
        elif totalSpent > 0 and totalSpent < 100:
            return "A"
    

