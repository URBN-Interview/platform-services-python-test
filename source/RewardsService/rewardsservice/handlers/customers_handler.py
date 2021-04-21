import json
from abc import ABC

import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

"""Gets all the customers"""
class customersHandler(tornado.web.RequestHandler, ABC):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]
        customers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(customers))