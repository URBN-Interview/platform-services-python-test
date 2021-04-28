import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomersHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        col = db["Customers"]
        cursor = col.find()
        matches = list(cursor)
        if(len(matches)==0):
            self.write("No Users Exist in the DB")
        else:
            self.write(str(matches))

    def encodeList(self, d):
        print(d)
        for item in d:
            if '_id' in item:
                item['_id'] = str(item['_id'])
        return d
