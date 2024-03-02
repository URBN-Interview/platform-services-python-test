import json
from bson import ObjectId
from pymongo import MongoClient

from tornado.escape import json_encode, json_decode
from tornado.gen import coroutine
import tornado.web


class CustomerRewardsHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.client = MongoClient("mongodb", 27017)
        self.db = self.client['Rewards']

    @staticmethod
    def _calculate_points(amount, available_points=0):
        return int(amount or 0) + available_points

    def get_customer_available_points(self, email):
        customer = self.db.customers.find_one({"email": email})
        return customer.get("points") if customer else 0

    @coroutine
    def post(self):
        customer = json_decode(self.request.body)
        available_points = self.get_customer_available_points(customer.get("emailId"))
        points = self._calculate_points(customer.get("orderTotal"), available_points)
        reward = ""
        customer.update({
            "_id": str(ObjectId()),
            "points": points,
            "tier": "",
            "rewardName": "",
            "nextTier": "",
            "nextRewardName": "",
        })

        del customer["orderTotal"]
        created_customer = self.db.customers.insert_one(customer)
        self.set_status(201)
        self.write(json_encode({"message": "Customer rewards created/updated successfully!"}))
