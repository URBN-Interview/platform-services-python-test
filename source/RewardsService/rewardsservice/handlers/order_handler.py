import json
from tornado import web, escape

from pymongo import MongoClient
from tornado.gen import coroutine



class OrderHandler(web.RequestHandler):    
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        body = escape.json_decode(self.request.body)
        customer_email = body["data"]["customer_email"]
        order_total = body["data"]["order_total"]
        order = {
            "email_address": customer_email, 
            "order_total": order_total
        }
        db.rewards.insert_one(order)
        self.write("added an order")