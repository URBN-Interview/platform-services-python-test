import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class AllCustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        dbCustomer = db["Customers"]

        customers = list(dbCustomer.find({}, {"_id" : 0}))
        
        self.write(json.dumps(customers))
