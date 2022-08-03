import math
import re

from pymongo import MongoClient

class RewardsDataHelper():
    def __init__(self):
        self.client = MongoClient("mongodb", 27017)
        self.db = self.client["Rewards"]

    # find_new_tier determines which rewards tier a customer
    # lands in depending on the number of points they have earned.
    def find_new_tier(self, points):
        # default_tier represents the customer's rewards_tier before they have
        # earned enough points to qualify for the first rewards_tier (tier A)
        default_tier = {"tier": None, "rewardName": None, "points": 0}

        # Finds the first rewards_tier that is less than or equal to the customer's
        # current number of rewards points
        new_tier = list(self.db.rewards.find({"points": {"$lte": points}}).sort("points", -1).limit(1))
        
        # If the customer doesn't yet qualify for the first tier, return
        # the default tier. Otherwise, return the tier matching the customer's
        # total points.
        if not new_tier:
            return default_tier
        else:
            return new_tier[0]
    
    # find_next_tier determines what the next rewards_tier is
    # for a customer based on the number of points they have earned
    def find_next_tier(self, points):
        # final_fron_tier is used when a customer has already reached the
        # highest rewards tier
        final_fron_tier = {"tier": None, "rewardName": None, "points": None}

        # Finds the first rewards_tier that is greater than the customer's
        # current number of rewards points
        next_tier = list(self.db.rewards.find({"points": {"$gt": points}}).sort("points", 1).limit(1))
        
        # If the customer has already hit the highest rewards tier, return
        # the final_fron_tier. Otherwise, return the next tier the customer
        # is eligible to reach.
        if not next_tier:
            return final_fron_tier
        else:
            return next_tier[0]

    # calculate_next_tier_progress returns the percentage progress
    # towards the customer's next rewards_tier. Ex:
    # points=150, new_tier_points=100, next_tier_points=200 will return 0.5
    def calculate_next_tier_progress(self, points, new_tier_points, next_tier_points):
        # returns None if the customer has already reached the max
        # rewards tier
        if not next_tier_points:
            return None
        else:
            return (points%(next_tier_points - new_tier_points))/100.0

    def validate_input(self, email_address, order_total):
        email_reg = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if not re.match(email_reg, email_address):
            return False, "invalid email address"
        
        try:
            points = int(order_total)
            if points < 0:
                return False, "order total cannot be negative"
        except ValueError:
            return False, "order total must be a number"

        return True, None
        