#!/usr/bin/env python
#endpoint 2
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class GetCustomerHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        """
        TODO: Get a single customer's data from database.

        Returns
        -------
        json
            Return a single customer's data using email from input argument.
        """

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        email = self.get_argument("email")
        findEmailQuery = {"email": email}

        myCustomer = db.orders.find_one(findEmailQuery, {"_id": 0})

        if myCustomer is not None:
            self.write(json.dumps(myCustomer))
