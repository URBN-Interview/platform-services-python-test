from rewardsservice.handlers.base_handler import BaseHandler
from rewardsservice.repositories.rewards_repository import RewardsRepository

class RewardsHandler(BaseHandler):

    def initialize(self, repo: RewardsRepository):
        self.repo = repo

    async def get(self):
        rewards = await self.repo.get_all_tiers()
        self.write_json(rewards)
