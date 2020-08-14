#get_all_customer_handler.py
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class AllCustomer(tornado.web.RequestHandler):

    def get(self):
        # self.set_header("Content-Type", "application/json")
        client = MongoClient("mongodb", 27017)
        db = client['Customers']
        allcustomers = list(db.Customers.find({}, {'_id': 0}))
        self.write(json.dumps(allcustomers))