import json
import tornado.web
import pprint

from pymongo import MongoClient
from tornado.gen import coroutine
from bson import json_util

class CustomerRequest(tornado.web.RequestHandler):
    @coroutine
    def get(self, email_id):
        #Connection to MongoDB
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]

        cust_data = db.customers.find_one({"email":email_id})

        if cust_data!=None:
            self.write(json_util.dumps(cust_data))
        else:
            self.write("Email ID not in the database")
        
