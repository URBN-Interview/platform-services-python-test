import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class SingleCustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer_email = self.get_argument("email_address")
        customer = db.orders.find_one({"emailAddress": customer_email})
        self.write(json.dumps(customer, default=str))


class AllCustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.orders.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
