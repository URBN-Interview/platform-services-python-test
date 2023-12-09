from decimal import Decimal
import json
from tornado import web, escape

from pymongo import MongoClient
from tornado.gen import coroutine

CLIENT = MongoClient("mongodb", 27017)

class OrderHandler(web.RequestHandler):    
    def post(self):
        db = CLIENT["Rewards"]
        body = escape.json_decode(self.request.body)
        customer_email = body["data"]["customer_email"]
        order_total = body["data"]["order_total"]
        order = {
            "email_address": customer_email, 
            "order_total": order_total
        }
        self.rewards_calculation(order)
        self.write("added an order")

    def rewards_calculation(self, order):
        db = CLIENT["Rewards"]
        order_total = int(Decimal(order["order_total"]))
        print(db.rewards.find_one({"points": order_total}))