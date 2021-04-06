import json
import tornado.web
import pprint

from pymongo import MongoClient
from tornado.gen import coroutine
from bson import json_util


class AllCustomerRequests(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        #Connection to MongoDB
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]

        #Get all the documents and send the response back in JSON format
        cust_data  = list(db.customers.find({}))
        self.write(json_util.dumps(cust_data))
