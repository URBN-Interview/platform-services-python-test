import json
import tornado.web
import math

from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsDataHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.client = MongoClient("mongodb", 27017)
        self.db = self.client["Rewards"]

    @coroutine
    def get(self, email):
        rewards_data = self.db.rewards_data.find_one({}, {"email_address": email})
        self.write(json.dumps(rewards_data))
    
    @coroutine
    def post(self):
        email = self.get_body_argument("email_address")
        order_total = float(self.get_body_argument("order_total"))
        points_earned = math.floor(order_total)

        query = {"email_address": email}
        rewards_data = self.db.rewards_data.find_one(query)
        if rewards_data == None:
            new_tier = list(self.db.rewards.find({"points": {"$lte": points_earned}}).sort("points", -1).limit(1))
            if not new_tier:
                new_tier = {"tier": None, "rewardName": None, "points": 0}
                next_tier = list(self.db.rewards.find({}, {"_id": 0}))[0]
            else:
                new_tier = new_tier[0]
                next_tier = list(self.db.rewards.find({"points": {"$gt": points_earned}}).sort("points", 1).limit(1))[0]

            self.db.rewards_data.insert({
                "email_address": email,
                "reward_points": points_earned,
                "reward_tier": new_tier["tier"],
                "reward_tier_name": new_tier["rewardName"],
                "next_reward_tier": next_tier["tier"],
                "next_reward_tier_name": next_tier["rewardName"],
                "next_reward_tier_progress": (points_earned%(next_tier["points"] - new_tier["points"]))/100.0
            })
        else:
            new_points_total = rewards_data["reward_points"] + points_earned
            new_tier = list(self.db.rewards.find({"points": {"$lte": new_points_total}}).sort("points", -1).limit(1))
            if not new_tier:
                new_tier = {"tier": None, "rewardName": None, "points": 0}
                next_tier = list(self.db.rewards.find({}, {"_id": 0}))[0]
            else:
                new_tier = new_tier[0]
                next_tier = list(self.db.rewards.find({"points": {"$gt": new_points_total}}).sort("points", 1).limit(1))[0]

            updated_values = { "$set": {
                "reward_points": new_points_total,
                "reward_tier": new_tier["tier"],
                "reward_tier_name": new_tier["rewardName"],
                "next_reward_tier": next_tier["tier"],
                "next_reward_tier_name": next_tier["rewardName"],
                "next_reward_tier_progress": (new_points_total%(next_tier["points"] - new_tier["points"]))/100.0
            }}
            self.db.rewards_data.update_one(query, updated_values)
        
        rewards_data = self.db.rewards_data.find_one(query)
        self.write(json.dumps(rewards_data, default=lambda o: '<not serializable>'))


