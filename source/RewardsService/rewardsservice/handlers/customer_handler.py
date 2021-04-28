import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        col = db["Customers"]

        email = self.get_arguments("email")[0]
        print('emailArg: {}'.format(email))
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
