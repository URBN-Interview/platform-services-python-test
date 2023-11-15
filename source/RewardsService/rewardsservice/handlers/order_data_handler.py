import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class OrderDataHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.client = MongoClient("mongodb", 27017)
        self.db = self.client["Rewards"]

    def create_order_doc(self, email, total) -> dict:
        order_doc = {
            "customerEmail": email,
            "customerOrderTotal": float(total),
        }
        return order_doc

    @coroutine
    def post(self):
        customer_email = self.get_argument("customerEmail")
        customer_order_total = self.get_argument("orderTotal")
        document = self.create_order_doc(customer_email, customer_order_total)
        self.write(json.dumps(document))
