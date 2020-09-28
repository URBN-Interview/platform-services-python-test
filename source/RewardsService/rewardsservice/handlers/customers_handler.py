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
        self.write(email)
        customerData = db.customers.find_one({"Email Address": email})

        if (not customerData):
            self.write("This must be an invalid input.")
        else:
            self.write({"Customer Data": customerData})
