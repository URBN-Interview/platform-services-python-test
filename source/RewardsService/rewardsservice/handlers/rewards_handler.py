import json

from pymongo import MongoClient
from .base_handler import BaseHandler

DB = BaseHandler.CLIENT["Rewards"]

class RewardsHandler(BaseHandler):

    async def get(self):
        rewards = list(DB.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards, indent=4))
