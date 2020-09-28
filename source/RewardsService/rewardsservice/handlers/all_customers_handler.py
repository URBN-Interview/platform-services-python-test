import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class AllCustomersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Customer"]
        allCustomers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(allCustomers))
