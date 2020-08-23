import json
import math
import tornado.web

from pymongo import MongoClient

class OrderCalculator():
    
    def get_email_record(self, email_address, db):
        email_address = db.orders.find_one({"emailAddress": email_address})
        return email_address

    def get_reward_points(self, order_amount):
        return math.floor(float(order_amount))

    def get_tier_record(self, reward_points):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        reward_points_nearest_hundred = math.floor(reward_points/100) * 100
        if reward_points_nearest_hundred < 100:
            tier = {"points": None, "rewardName": "No rewards yet", "tier": "N/A"}
        else:
            tier = db.rewards.find_one({"points": reward_points_nearest_hundred})
        return tier
    
    def get_next_tier_record(self, tier):
        next_tier_record = None
        if tier == 'A':
            next_tier_record = OrderCalculator.get_tier_record(self, 200)
        elif tier == 'B':
            next_tier_record = OrderCalculator.get_tier_record(self, 300)
        elif tier == 'C':
            next_tier_record = OrderCalculator.get_tier_record(self, 400)
        elif tier == 'D':
            next_tier_record = OrderCalculator.get_tier_record(self, 500)
        elif tier == 'E':
            next_tier_record = OrderCalculator.get_tier_record(self, 600)
        elif tier == 'F':
            next_tier_record = OrderCalculator.get_tier_record(self, 700)
        elif tier == 'G':
            next_tier_record = OrderCalculator.get_tier_record(self, 800)
        elif tier == 'H':
            next_tier_record = OrderCalculator.get_tier_record(self, 900)
        elif tier == 'I':
            next_tier_record = OrderCalculator.get_tier_record(self, 1000)
        elif tier == 'J':
            next_tier_record = {"points": None, "rewardName": "No more rewards to earn", "tier": "N/A"}
        else:
            next_tier_record = OrderCalculator.get_tier_record(self, 100)
        return next_tier_record

    def get_percentage_to_next_tier(self, reward_points, next_tier_points):
        if next_tier_points is None:
            return 0.0
        return (next_tier_points - reward_points) / 100