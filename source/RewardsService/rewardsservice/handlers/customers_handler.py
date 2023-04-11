import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomersHandler(tornado.web.RequestHandler):
    """
    Returns all the customers rewards data
    """

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["CustomerData"]
        customers = list(db.customerdata.find({}, {"_id": 0}))
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(customers))
