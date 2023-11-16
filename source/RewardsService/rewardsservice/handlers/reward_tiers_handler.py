import json

from tornado.gen import coroutine
from .rewards_base_handler import RewardsBaseHandler


class GetRewardTiersHandler(RewardsBaseHandler):
    @coroutine
    def get(self):
        rewards = list(self.db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
