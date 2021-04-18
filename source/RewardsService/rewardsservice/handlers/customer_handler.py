import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        email_address = self.get_argument("emailAddress")
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer_data = list(db.customers.find({"emailAddress": email_address}, {"_id": 0}))
        self.write(json.dumps(customer_data))
