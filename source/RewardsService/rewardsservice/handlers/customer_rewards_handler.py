import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerRewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]
        email_address = self.get_argument('email_address')
        customer_email_result = list(db.customers.find({"email_address": email_address}, {"_id":0}))
        self.write(json.dumps(customer_email_result))

