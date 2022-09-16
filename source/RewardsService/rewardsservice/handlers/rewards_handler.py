import json
import tornado.web

from tornado.gen import coroutine
from util.db_connection import DBConnection


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = DBConnection.get_client()
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
