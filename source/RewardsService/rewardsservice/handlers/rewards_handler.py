import json
from abc import ABC

import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

"""Gets the Rewards"""
class RewardsHandler(tornado.web.RequestHandler, ABC):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        db_customers = client["customers"]
        rewards = list(db.rewards.find({}, {"_id": 0}))+list(db_customers.Customers.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))