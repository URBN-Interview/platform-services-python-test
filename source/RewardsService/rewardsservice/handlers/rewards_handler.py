from handlers.base_handler import BaseHandler


class RewardsHandler(BaseHandler):
    """GET /rewards - list the reward tiers."""

    async def get(self):
        self.write_json(await self.repository.get_tiers())
