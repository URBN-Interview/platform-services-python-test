import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerDataHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer_data = list(db.customerdata.find({}, {"_id": 0}))
        self.write(json.dumps(customer_data))
