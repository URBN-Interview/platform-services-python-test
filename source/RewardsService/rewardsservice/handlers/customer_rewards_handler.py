import json
import tornado
from tornado.gen import coroutine
from pymongo import MongoClient
from rewardsservice.error_handling.error_handling import EmailErrorHandler


# get rewards data for all customers
class CustomerRewardsHandler(tornado.web.RequestHandler):    
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer_order_data_collection = db["customerOrderData"]
        res = list(customer_order_data_collection.find({}, {"_id": 0}))
        self.write(json.dumps(res))

# get rewards data for customer matching the given email
class SingleCustomerRewardsDataHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer_order_data_collection = db["customerOrderData"]
        result = tornado.escape.json_decode(self.request.body)

        validate_email = EmailErrorHandler()
        validation = validate_email.validate_email_address(result["Email Address"])
        
        if isinstance(validation, list):
            self.write(validation[0])

        else:

            customer_email_address = result["Email Address"]        
            res = list(customer_order_data_collection.find({"Email Address": customer_email_address}, {"_id": 0}))
            self.write(json.dumps(res))