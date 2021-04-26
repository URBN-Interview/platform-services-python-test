import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class Endpoint2(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)

        db = client["Rewards"]
        
        # grab all users
        users = list(db.users.find({}, {"_id": 0}))

        # get email
        email = self.get_query_argument('email')
        self.write(json.dumps(list(db.users.find({"email": {'$regex': email}}, {"_id": 0}))))
