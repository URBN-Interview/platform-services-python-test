import math

from pymongo import MongoClient

class RewardsDataHelper():
    def __init__(self):
        self.client = MongoClient("mongodb", 27017)
        self.db = self.client["Rewards"]

    def find_new_tier(self, points):
        default_tier = {"tier": None, "rewardName": None, "points": 0}
        new_tier = list(self.db.rewards.find({"points": {"$lte": points}}).sort("points", -1).limit(1))
        
        if not new_tier:
            return default_tier
        else:
            return new_tier[0]
    
    def find_next_tier(self, points):
        final_fron_tier = {"tier": None, "rewardName": None, "points": None}
        next_tier = list(self.db.rewards.find({"points": {"$gt": points}}).sort("points", 1).limit(1))
        
        if not next_tier:
            return final_fron_tier
        else:
            return next_tier[0]

    def calculate_next_tier_progress(self, points, new_tier_points, next_tier_points):
        if not next_tier_points:
            return None
        else:
            return (points%(next_tier_points - new_tier_points))/100.0
