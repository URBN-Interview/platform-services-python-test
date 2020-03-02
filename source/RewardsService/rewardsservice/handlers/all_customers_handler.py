import tornado.web
import json

from util.validation import Validaton
from pymongo import MongoClient
from tornado.gen import coroutine
from tornado.options import options

class AllCustomersHandler(tornado.web.RequestHandler):
    collectionName = 'Customers'

    @coroutine
    def get(self):
        client = MongoClient(options.mongodb_host)
        db = client[self.collectionName]
        customers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(customers))
