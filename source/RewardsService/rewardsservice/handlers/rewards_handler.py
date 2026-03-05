import json
import tornado.web

from pymongo import MongoClient


class RewardsHandler(tornado.web.RequestHandler):

    async def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
