import tornado.web
import json

from util.validation import Validaton
from pymongo import MongoClient
from tornado.gen import coroutine
from tornado.options import options

class CustomersHandler(tornado.web.RequestHandler):
    collectionName = 'Customers'

    @coroutine
    def post(self):
        client = MongoClient(options.mongodb_host)
        db = client[self.collectionName]
        validation = Validaton()

        email = str(self.get_argument('email', ''))
        orderTotal = str(self.get_argument('orderTotal', ''))

        validation.emailValidation(email).currencyValidation(orderTotal).validate()
        customer = db.customers.insert({"email": email, "orderTotal": orderTotal})

        self.write({"email": email, "orderTotal": orderTotal})

    @coroutine
    def get(self):
        client = MongoClient(options.mongodb_host)
        db = client[self.collectionName]
        validation = Validaton()
        email = str(self.get_argument('email', ''))

        if email :
            validation.emailValidation(email).validate()
            customers = db.customers.find_one({"email": email}, {"_id": 0})
        else:
            customers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(customers))
