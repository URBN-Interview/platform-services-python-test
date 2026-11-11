# Request handler for the /rewards endpoint, which exposes the reward tier
# definitions (tier letter, reward name, points required) stored in MongoDB.

import json

from handlers.base_handler import BaseHandler


class RewardsHandler(BaseHandler):
    """Serves /rewards.

    GET: returns every reward tier from the Rewards.rewards collection as a
    JSON list (the Mongo _id field is excluded).
    """

    async def get(self):
        # Shared Motor client from App; awaiting keeps the event loop free
        rewards = await self.application.db.rewards.find({}, {"_id": 0}).to_list(None)

        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(rewards))
