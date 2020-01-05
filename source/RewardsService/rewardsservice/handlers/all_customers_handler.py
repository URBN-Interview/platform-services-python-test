import tornado.web
import json

from pymongo import MongoClient
from tornado.gen import coroutine


class AllCustomersHandler(tornado.web.RequestHandler):
    """Returns all customers reward info"""

    @coroutine
    def get(self):
        """Accesses and returns list of all customers rewards info"""
        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            customers = list(db.customers.find({}, {"_id": 0}))
            self.write(json.dumps(customers))
        except:
            print("Error finding all customers info")
