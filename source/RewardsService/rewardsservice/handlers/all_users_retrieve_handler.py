import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class AllUsersRetrieveHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        all_user_info = list(db.user_info.find({}, {"_id": 0}))
        self.write(json.dumps(all_user_info))
