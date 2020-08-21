import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
import math


#following OOD design best practices, I am creating a class to handle the customer operations and rewards
class CustomerHandler(tornado.web.RequestHandler):

    # updating this get method to get the data of a single customer
    @coroutine
    def get(self): 
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]
        email_address = self.get_argument("emailAddress", None)
        if not email_address:
            self.write("This email doesn't exist in the system!")
        else: 
          self.write(db.customers.find_one({"emailAddress": email_address}, {"_id": 0}))


    # Adding this post method to add an order for an existing customer else create a new customer
    @coroutine
    def post(self): 
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]
        email_address = self.get_argument("emailAddress", None)
        order_total = self.get_argument("orderTotal", None)
        if not email_address:
            self.write("This email doesn't exist in the system! Adding new customer")
            # insert a new one to the database
            db.customers.insert({"emailAddress": email_address}, {"rewardPoints": order_total})
        else: 
          self.write(db.customers.find_one({"emailAddress": email_address}, {"_id": 0}))







