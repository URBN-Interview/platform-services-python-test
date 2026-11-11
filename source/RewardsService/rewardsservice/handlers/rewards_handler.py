# Request handler for the /rewards endpoint, which exposes the reward tier
# definitions (tier letter, reward name, points required) stored in MongoDB.

import json

from pymongo import MongoClient

from handlers.base_handler import BaseHandler


class RewardsHandler(BaseHandler):
    """Serves /rewards.

    GET: returns every reward tier from the Rewards.rewards collection as a
    JSON list (the Mongo _id field is excluded).
    """

    async def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
