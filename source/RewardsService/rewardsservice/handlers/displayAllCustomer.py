import json
import tornado.web
import math

from pymongo import MongoClient
from tornado.gen import coroutine


class displayCustomer(tornado.web.RequestHandler):
    client = MongoClient("mongodb", 27017)
    db = client["Customer"]
    email = self.get_arguments("email")
    users = db.find()
    if(not users):
        self.write("No users found")
    else:
        (self.write(json.dumps(users)))
