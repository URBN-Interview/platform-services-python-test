#!/usr/bin/env python
#endpoint 2
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class GetCustomerHandler(tornado.web.RequestHandler):
    #get single customer data

    @coroutine
    def getCustomer(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        #get email & write query
        email = self.get_argument("email")
        findEmailQuery = {"email": email}

        #check db to see if it exsists
        myCustomer = db.customers.find_one(findEmailQuery)

        if customer is not None:
            self.write(json.dumps(myCustomer))
