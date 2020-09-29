import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class CustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        dbCustomer = db["Customers"]

        email = self.get_argument("email", "")

        customer = dbCustomer.find_one({"email" : email}, {"_id" : 0})
        
        if(customer is not None) :
            self.write(json.dumps(customer))
        else :
            self.write("email does not exist")
