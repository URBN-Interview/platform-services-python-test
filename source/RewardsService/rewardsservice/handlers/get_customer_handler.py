# get_customer_handler
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class GetCustomer(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        self.set_header("Content-Type", "application/json")
        client = MongoClient("mongodb", 27017)
        db = client['Customers']
        email = self.get_body_argument('emailAddress', None)
        customer = db.Customers.find_one({'emailAddress': email}, {'_id': 0})
        self.write(json.dumps(customer))
    

