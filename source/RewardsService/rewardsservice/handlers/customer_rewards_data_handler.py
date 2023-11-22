import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
from tornado.web import HTTPError, MissingArgumentError

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

        # find the datapoint(s) in the customers collection that contains the email given in the argument
        matching_emails = []
        try:
            email = self.get_argument("email")
        except MissingArgumentError as e:
            self.write_error(e.status_code)
            return

        for customer in customers:
            if email in customer.values():
                matching_emails.append(customer)

        try:
            self.write(json.dumps(matching_emails))
        except HTTPError:
            return
