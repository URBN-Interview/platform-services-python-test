import json

from handlers.base_handler import BaseHandler


class RewardsHandler(BaseHandler):

    async def get(self):
        rewards = await self.application.db.rewards.find({}, {"_id": 0}).to_list(length=None)
        self.write(json.dumps(rewards))
