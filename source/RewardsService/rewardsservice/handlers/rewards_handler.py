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


class OrderDatatHandler(tornado.web.RequestHandler):
    """Endpoint which accepts a customers email adress, and order total, and stores
    the their rewards data based on the amount of points they have. """
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        # Using the argument method to accept customer email & order total.
        email_address = self.get_argument("email_address")
        order_total = self.get_argument("order_total")
        # For each dollar a customer spends, the customer will earn 1 reward point.
        points = order_total * 1
