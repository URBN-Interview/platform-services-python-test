import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

"""
Endpoint 2: 
    * Accept a customer's email address, and return the customer's rewards data that was stored in Endpoint 1.
"""
class CustomerRewardsDataHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customers = list(db.customers.find({}, {"_id": 0}))

        matching_emails = []
        try:
            email = self.get_argument("email")
            for customer in customers:
                if email in customer.values():
                    matching_emails.append(customer)
            self.write(json.dumps(matching_emails))
        except ValueError:
            return
