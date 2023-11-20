import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

"""
Endpoint 3: 
    * Return the same rewards data as Endpoint 2 (CustomerRewardsDataHandler) but for all customers.
"""

class RewardsDataHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(customers))
