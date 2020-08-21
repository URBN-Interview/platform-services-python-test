import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


#following OOD design best practices, I am creating a class to handle the customer operations and rewards
class CustomerHandler(tornado.web.RequestHandler):

    # updating this get method to get the data of a single customer
    @coroutine
    def get(self): 
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]
        emailAddress = "test2@test.com"
        emailAddress = self.get_argument("emailAddress", None)
        if not emailAddress:
            self.write("This email doesn't exist in the system!")
        else: 
          self.write(db.customers.find_one({"emailAddress": emailAddress}, {"_id": 0}))


    # Adding this post method to add an order for an existing customer else create a new customer
    @coroutine
    def post(self): 
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]
        emailAddress = self.get_argument("emailAddress", None)
        orderTotal = self.get_argument("orderTotal", None)
        if not emailAddress:
            self.write("This email doesn't exist in the system! Adding new customer")
            # insert a new one to the database
            db.customers.insert({"emailAddress": emailAddress}, {"rewardPoints": orderTotal})
        else: 
          self.write(db.customers.find_one({"emailAddress": emailAddress}, {"_id": 0}))







