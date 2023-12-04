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

class CustomersHandler(tornado.web.RequestHandler):

    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(customers))

class CustomerHandler(tornado.web.RequestHandler):

    def get(self, customerEmail):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer = db.customers.find({"email": customerEmail})
        self.write(json.dump(customer))
