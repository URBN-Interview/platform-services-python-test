import json
import tornado
from tornado.gen import coroutine
from pymongo import MongoClient



class CustomerRewardsHandler(tornado.web.RequestHandler):    
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer_order_data_collection = db["customerOrderData"]
        res = list(customer_order_data_collection.find({}, {"_id": 0}))
        self.write(json.dumps(res))


class SingleCustomerRewardsDataHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer_order_data_collection = db["customerOrderData"]
        result = tornado.escape.json_decode(self.request.body)
        customer_email_address = result["Email Address"]        
        res = list(customer_order_data_collection.find({"Email Address": customer_email_address}, {"_id": 0}))
        self.write(json.dumps(res))