import logging
import tornado.gen

from pymongo import MongoClient


class RewardTierUtil:
    """
    RewardTierUtil is a collection of assistant functions for
    identifying, calculating, and updating customer reward levels
    in the Rewards Service
    """

    def __init__(self):
        self.client = MongoClient("mongodb", 27017)
        self.db = self.client["Rewards"]
        self.logger = logging.getLogger()

    def calculate_tiers(self, point_total: int) -> dict:
        """
        Return a dictionary with the current and upcoming tier
        values for the user query. Requires a 'point_total'
        representing the current users points
        """

        # get it - no tears. like the shampoo. i wrote this at 10pm
        loreal = {"tier": "", "rewardName": "", "points": None}
        max_tier = {"tier": "J", "rewardName": "50% off purchase", "points": 1000}

        check_current_tier = self.db.rewards.find_one(
            {"points": {"$lte": point_total}}, sort=[("points", -1)]
        )
        if check_current_tier:
            current_tier = check_current_tier["tier"]
            current_tier_name = check_current_tier["rewardName"]
        else:
            current_tier = loreal["tier"]
            current_tier_name = loreal["rewardName"]

        check_next_tier = self.db.rewards.find_one(
            {"points": {"$gt": point_total}}, sort=[("points", 1)]
        )

        if check_next_tier:
            next_tier = check_next_tier["points"]
            next_tier_name = check_next_tier["rewardName"]
            next_tier_points = check_next_tier["points"]
        else:
            next_tier = max_tier["points"]
            next_tier_name = max_tier["rewardName"]
            next_tier_points = max_tier["points"]

        # I felt that it made more sense to return
        # how much progress the customer has made towards
        # their next tier, as opposed to a
        # percentage deficit from. If I saw something like
        # 88% progress towards next goal,
        # I'd be more inclined to 'complete the goal'
        return {
            "tier": current_tier,
            "tierName": current_tier_name,
            "nextTier": next_tier,
            "nextTierName": next_tier_name,
            "nextTierProgress": (100 - (next_tier_points - point_total)) / 100,
        }

    @tornado.gen.coroutine
    def hydrate_document(
        self,
        points: int,
        email: str,
    ) -> dict:
        """
        hydrate_document returns a dictionary object representing
        a hydrated mongoDB document ready for insertion into a named
        db collection
        """

        tiers = self.calculate_tiers(points)

        hydrated_doc = {
            "email": email,
            "points": points,
            "tier": tiers["tier"],
            "tierName": tiers["tierName"],
            "nextTier": tiers["nextTier"],
            "nextTierName": tiers["nextTierName"],
            "nextTierProgress": tiers["nextTierProgress"],
        }
        raise tornado.gen.Return(hydrated_doc)
