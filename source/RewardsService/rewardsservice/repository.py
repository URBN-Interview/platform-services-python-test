"""MongoDB data access for reward tiers and customer rewards (async, via Motor)."""
from pymongo import ReturnDocument

import rewards_calculator

CUSTOMER_FIELDS = {"_id": 0}


class RewardsRepository:

    def __init__(self, db):
        self.db = db

    async def ensure_indexes(self):
        await self.db.customers.create_index("email", unique=True)

    async def get_tiers(self):
        cursor = self.db.rewards.find({}, {"_id": 0}).sort("points", 1)
        return await cursor.to_list(length=None)

    async def get_customer(self, email):
        return await self.db.customers.find_one({"email": email}, CUSTOMER_FIELDS)

    async def get_customers(self):
        cursor = self.db.customers.find({}, CUSTOMER_FIELDS).sort("email", 1)
        return await cursor.to_list(length=None)

    async def add_order(self, email, order_total):
        """Credit an order to a customer and store their recalculated rewards.

        Points are added with an atomic, capped update so concurrent orders for
        the same customer are never lost. The derived tier fields are then
        written only if the points are still the value we calculated from, so a
        slower request cannot overwrite a newer one with stale data.
        """
        tiers = await self.get_tiers()
        if not tiers:
            raise RuntimeError("No reward tiers are configured")

        earned = rewards_calculator.points_for_order(order_total)
        cap = rewards_calculator.max_points(tiers)

        updated = await self.db.customers.find_one_and_update(
            {"email": email},
            [{"$set": {
                "email": email,
                "points": {"$min": [{"$add": [{"$ifNull": ["$points", 0]}, earned]}, cap]},
            }}],
            upsert=True,
            projection=CUSTOMER_FIELDS,
            return_document=ReturnDocument.AFTER,
        )

        rewards = rewards_calculator.calculate_rewards(email, updated["points"], tiers)
        await self.db.customers.update_one(
            {"email": email, "points": rewards["points"]},
            {"$set": rewards},
        )
        return rewards
