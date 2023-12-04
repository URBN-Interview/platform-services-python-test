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

class CustomerListHandler(tornado.web.RequestHandler):

    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(customers))

class CustomerHandler(tornado.web.RequestHandler):

    def get(self, email):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer = db.customers.find_one({"email": email}, {"_id": 0})
        if customer:
            self.write(json.dumps(customer))
        else:
            raise tornado.web.HTTPError(404, log_message="Customer does not exist")

    def put(self, email):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer = db.customers.find_one({"email": email}, {"_id": 0})
        response = tornado.escape.json_decode(self.request.body)
        total = response["total"]
        new_points = customer["points"] + total
        customer["points"] = new_points
        db.customers.update_one({"email": email}, {"$set": customer})
        updated_customer = db.customers.find_one({"email": email}, {"_id": 0})
        self.write(json.dumps(updated_customer))
