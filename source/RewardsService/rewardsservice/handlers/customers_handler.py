import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]
        customers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(customers))

