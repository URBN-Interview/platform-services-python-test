import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
from util.server_error import UnknownError

class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))

    def write_error(self, status_code, **kwargs):
        if status_code == 500 and not self.error:
            self.error = UnknownError()
        self.write({"type" : self.error.type, "context": self.error.context, "error": self.error.error})
