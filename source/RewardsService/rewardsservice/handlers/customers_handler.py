import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customersList = list(db.customers.finds({}))
        print("all customers: ", customersList)
        self.write(json.dumps(customersList))
