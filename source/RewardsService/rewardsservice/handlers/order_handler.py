import json

import tornado
from mongo.mongo_manager import MongoManager
from tornado.gen import coroutine


class OrderHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client =  MongoManager().client
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
