import tornado.web
import json

from util.validation import Validaton
from pymongo import MongoClient
from tornado.gen import coroutine
from tornado.options import options

class OrderHandler(tornado.web.RequestHandler):
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