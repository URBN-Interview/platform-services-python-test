import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

# This class handles **Endpoint 3:** and returns all customer information
# No parameters are needed.
class AllCustomersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]
        customers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(customers))
