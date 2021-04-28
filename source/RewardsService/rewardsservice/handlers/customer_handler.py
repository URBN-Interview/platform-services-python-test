import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerHandler(tornado.web.RequestHandler):
    """ CustomerHandler
    GET:
        summary: Accepts a customer's email, returns customer tier information
        url: /customer/
        parameters:
            - email adress (string)
        responses:
            500:
                Internal Server Error (default)
            400:
                Empty email provided
                Invalid email (missing @)
    """
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        col = db["Customers"]

        email = self.get_arguments("email")
        print('emailArg: {}'.format(email))
        email = email[0] if isinstance(email, list) else email

        #raise 400 error if email is empty or invalid
        if len(email)==0 or not '@' in email:
            raise tornado.web.HTTPError(400)

        cursor = col.find({"email": email})
        matches = list(cursor)
        if(len(matches)==0):
            self.write("Email Address doesn't exist in DB")
        else:
            print(matches[0])
            self.write(self.encode(matches[0]))

    def encode(self, o):
            if '_id' in o:
                o['_id'] = str(o['_id'])
            return o
