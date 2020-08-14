#delete_customer_handler.py
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class DeleteCustomer(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        # handles errors for foregin email and orderTotal input 
        self.write('<html><body><form action="/del" method="POST">'
        '<label for="email">Enter your email: </label>'
            '<input type="email" name="email"> '
            '<input type="submit" value="Submit">'
            '</form></body></html>')


    def post(self):
        self.set_header("Content-Type", "application/json")
        client = MongoClient("mongodb", 27017)
        db = client['Customers']
        email = self.get_body_argument('email', None)
        customer = db.Customers.find_one({'emailAddress': email}, {'_id': 0})
        if customer == None:
            self.write("Customer is not in the database")
        else:
            self.write( email + "  has been deleted")
            db.Customers.delete_one(customer)
