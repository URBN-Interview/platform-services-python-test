#!/usr/bin/env python
#endpoint 3
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class GetAllCustomersHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        """
        TODO: Get all customer data from database.

        Returns
        -------
        json
            Return a list of all customers from db.
        """

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        myCustomers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(myCustomers))
