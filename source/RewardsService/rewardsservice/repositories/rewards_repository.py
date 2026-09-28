import pymongo

HIDE_ID = {"_id": 0}

class RewardsRepository:
    """ Shared repository class for interacting with the rewards collection """
    def __init__(self, db):
        self.collection = db["rewards"]

    async def get_all_tiers(self):

        cursor = self.collection.find({}, HIDE_ID).sort("points", pymongo.ASCENDING)

        tiers = [tier async for tier in cursor]
        return tiers
