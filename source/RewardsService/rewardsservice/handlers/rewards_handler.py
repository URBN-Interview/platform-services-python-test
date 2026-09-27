from rewardsservice.handlers.base_handler import BaseHandler
from rewardsservice.repositories.rewards_repository import RewardsRepository

class RewardsHandler(BaseHandler):

    async def get(self, repo: RewardsRepository):
        rewards = repo.get_all_tiers
        self.write_json(rewards)
