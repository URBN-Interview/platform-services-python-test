import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

from helpers.rewards_helper import update_rewards


class OrdersHandler(tornado.web.RequestHandler):
    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        body = json.loads(self.request.body.decode('utf-8'))
        email, amount = body["email"], int(body["amount"])

        db.orders.insert_one({"email": email, "amount": amount})
        update_rewards(email)
