import json
import tornado.web
from bson import json_util
from pymongo import MongoClient
from tornado.gen import coroutine


class AdminHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        resObject = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(resObject))
