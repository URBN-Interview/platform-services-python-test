import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class SingleCustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customerData = json.loads(self.request.body)
        customers = list(db.customers.find(customerData.email))
        #print("customers", customers)
        self.write(json.dumps(customers))
    

    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        collist = db.list_collection_names()
            if "customers" in collist:
                customerData = json.loads(self.request.body)
                print("req.body data: ", customerData)
                db.customer.insert(customerData)

            else:
                customers = db["customers"]
                customerData = json.loads(self.request.body)
                db.customer.insert(customerData)