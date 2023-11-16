import json

from tornado.gen import coroutine
from .rewards_base_handler import RewardsBaseHandler


class GetRewardTiersHandler(RewardsBaseHandler):
    """
    GetRewardTiersHandler simply returns all available rewards
    from the rewards collection. It expects no params
    """

    @coroutine
    def get(self):
        rewards = list(self.db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
