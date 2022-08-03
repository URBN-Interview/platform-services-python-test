import json
import tornado.web
import math

from pymongo import MongoClient
from tornado.gen import coroutine
from helpers.rewards_data_helper import RewardsDataHelper


class RewardsDataHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.client = MongoClient("mongodb", 27017)
        self.db = self.client["Rewards"]
        self.helper = RewardsDataHelper()

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
            new_tier = self.helper.find_new_tier(points_earned)
            next_tier = self.helper.find_next_tier(points_earned)
            next_tier_progress = self.helper.calculate_next_tier_progress(points_earned, new_tier["points"], next_tier["points"])

            self.db.rewards_data.insert({
                "email_address": email,
                "reward_points": points_earned,
                "reward_tier": new_tier["tier"],
                "reward_tier_name": new_tier["rewardName"],
                "next_reward_tier": next_tier["tier"],
                "next_reward_tier_name": next_tier["rewardName"],
                "next_reward_tier_progress": next_tier_progress
            })
        else:
            new_points_total = rewards_data["reward_points"] + points_earned
            new_tier = self.helper.find_new_tier(new_points_total)
            next_tier = self.helper.find_next_tier(new_points_total)
            next_tier_progress = self.helper.calculate_next_tier_progress(new_points_total, new_tier["points"], next_tier["points"])

            updated_values = { "$set": {
                "reward_points": new_points_total,
                "reward_tier": new_tier["tier"],
                "reward_tier_name": new_tier["rewardName"],
                "next_reward_tier": next_tier["tier"],
                "next_reward_tier_name": next_tier["rewardName"],
                "next_reward_tier_progress": next_tier_progress
            }}
            self.db.rewards_data.update_one(query, updated_values)
        
        rewards_data = self.db.rewards_data.find_one(query)
        self.write(json.dumps(rewards_data, default=lambda o: '<not serializable>'))


