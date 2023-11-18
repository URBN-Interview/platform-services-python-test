import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        email = self.get_argument("email")
        order_total = float(self.get_argument("order_total"))

        # Calculate reward points based on order total (1 point per dollar)
        reward_points = int(order_total)

        # Logic to determine Reward Tier, Reward Tier Name, Next Reward Tier, Next Reward Tier Name, Next Reward Tier Progress

        reward_tiers = [
            {"tier": "A", "rewardName": "5% off purchase", "points": 100},
            {"tier": "B", "rewardName": "10% off purchase", "points": 200},
            {"tier": "C", "rewardName": "15% off purchase", "points": 300},
            {"tier": "D", "rewardName": "20% off purchase", "points": 400},
            {"tier": "E", "rewardName": "25% off purchase", "points": 500},
            {"tier": "F", "rewardName": "30% off purchase", "points": 600},
            {"tier": "G", "rewardName": "35% off purchase", "points": 700},
            {"tier": "H", "rewardName": "40% off purchase", "points": 800},
            {"tier": "I", "rewardName": "45% off purchase", "points": 900},
            {"tier": "J", "rewardName": "50% off purchase", "points": 1000}
        ]
        
        # Find the reward tier for the customer based on their earned points
        reward_tier = None
        reward_tier_name = None
        next_reward_tier = None
        next_reward_tier_name = None
        next_reward_tier_progress = None

        for tier_data in reward_tiers:
            if reward_points >= tier_data["points"]:
                reward_tier = tier_data["tier"]
                reward_tier_name = tier_data["rewardName"]

         # Find next reward tier details if applicable
        if reward_tier:
            next_tier_index = ord(reward_tier) - ord("A") + 1
            if next_tier_index < len(reward_tiers):
                next_reward_tier_data = reward_tiers[next_tier_index]
                next_reward_tier = next_reward_tier_data["tier"]
                next_reward_tier_name = next_reward_tier_data["rewardName"]
                points_needed = next_reward_tier_data["points"]
                next_reward_tier_progress = (points_needed - reward_points) / points_needed


        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        db.customer_rewards.insert({
            "email": email,
            "reward_points": reward_points,
            "reward_tier": reward_tier,
            "reward_tier_name": reward_tier_name,
            "next_reward_tier": next_reward_tier,
            "next_reward_tier_name": next_reward_tier_name,
            "next_reward_tier_progress": next_reward_tier_progress
        })
        self.write("Customer rewards data stored successfully.")


    

    # def get(self):
    #     client = MongoClient("mongodb", 27017)
    #     db = client["Rewards"]
    #     rewards = list(db.rewards.find({}, {"_id": 0}))
    #     self.write(json.dumps(rewards))
