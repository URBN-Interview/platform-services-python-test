import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Customer"]

        email = self.get_argument("email","")
        customerData = db.customers.find_one({"Email Address": email})

        if (not customerData):
            self.write("No customer with corresponding email.")
        else:
            self.write({"Customer Data": customerData})
