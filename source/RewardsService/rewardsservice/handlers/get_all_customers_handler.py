#!/usr/bin/env python
#endpoint 3
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class GetAllCustomersHandler(tornado.web.RequestHandler):
    #get all customer data

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        # get all my customers data & turn it into a list
        myCustomers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(myCustomers))
