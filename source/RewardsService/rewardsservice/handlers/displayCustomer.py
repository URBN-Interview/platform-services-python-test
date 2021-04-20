import json
import tornado.web
import math

from pymongo import MongoClient
from tornado.gen import coroutine


class displayCustomer(tornado.web.RequestHandler):
    client = MongoClient("mongodb", 27017)
    db = client["Customer"]
    email = self.get_arguments("email")
    user = db.find({"email": email})
    if(not user):
        self.write("No user with provided Email ID found")
    else:
        (self.write(json.dumps(user)))
