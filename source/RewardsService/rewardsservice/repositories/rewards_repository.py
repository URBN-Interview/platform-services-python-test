import pymongo

HIDE_ID = {"_id": 0}

class RewardsRepository:
    """ Shared repository class for interacting with the rewards collection """
    def __init__(self, db):
        self.collection = db["rewards"]

    async def get_current_tier(self, customer_points):
        query = {"points": {"$lte": customer_points}}

        # if the customer does not have enough points for tier A,
        # provide a "null" tier
        null_tier = {"tier": None, "rewardName": None, "points": 0}

        tier = await self.collection.find_one(query, HIDE_ID, sort=[("points", -1)])

        # if no tier is returned from the query, return the null tier
        # as the customer is not yet qualified for rewards
        if not tier:
            return null_tier
        else:
            return tier

    async def get_all_tiers(self):

        cursor = self.collection.find({}).sort("points", pymongo.ASCENDING)

        tiers = [tier async for tier in cursor]
        return tiers

    async def get_next_tier(self, customer_points):
        query = {"points": {"$gt": customer_points}}

        # if a customer is already at the max tier, they can't go any higher
        # so we'd return a null tier
        max_tier = {"tier": None, "rewardName": None, "points": 0}

        next_tier = await self.collection.find_one(query, HIDE_ID, sort=[("points", 1)])


        if not next_tier:
            return max_tier
        else:
            return next_tier
