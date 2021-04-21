import json
from abc import ABC

import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

"""
    Returns the specific customer based on the email provided in the argument
"""
class specific_customerHandler(tornado.web.RequestHandler, ABC):

    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]
        email = self.get_argument("email", "")
        customers = list(db.customers.find({"email": email},{"_id": 0}))
        self.write(json.dumps(customers))

    get = post