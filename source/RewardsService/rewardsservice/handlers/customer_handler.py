"""
Customer handler for handling requests for customer data

GET:
    Returns all customers

POST:
    Accepts customer email address
    Returns award information

"""

import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class CustomerHandler(tornado.web.RequestHandler):

    # return all customer
    @coroutine
    def get(self):
        json_response = {}

        try:
            client = MongoClient("mongodb", 27017)
        
            # get customers in customer collection from Rewards db
            db = client["Rewards"]
            customers = list(db.customers.find({}, {"_id": 0}))
            json_response = {"customers": customers}
        except Exception as err:
            raise err
        
        self.write(json.dumps(json_response))
    
    # return customer information from email
    @coroutine
    def post(self):
        json_response = {}

        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            
            # get post data
            json_request = tornado.escape.json_decode(self.request.body)

            if json_request["email"] == "":
                customer = list(db.customers.find({}, {"_id": 0}))
            else:
                customer = list(db.customers.find(
                    {"email": json_request["email"]},
                    {"_id": 0}
                ))

            json_response = {"customer": customer}
        except Exception as err:
            raise err

        self.write(json.dumps(json_response))
        