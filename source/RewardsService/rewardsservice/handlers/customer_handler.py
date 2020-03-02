import tornado.web
import json

from util.validation import Validaton
from pymongo import MongoClient
from tornado.gen import coroutine
from tornado.options import options

class CustomerHandler(tornado.web.RequestHandler):
    collectionName = 'Customers'
    
    @coroutine
    def get(self):
        client = MongoClient(options.mongodb_host)
        db = client[self.collectionName]
        
        email = str(self.get_argument('email', ''))
        Validaton().emailValidation(email).validate()

        customers = db.customers.find_one({"email": email}, {"_id": 0})
        self.write(json.dumps(customers))
