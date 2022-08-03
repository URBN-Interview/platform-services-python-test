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
    
    # POST with a payload of a customer's `email_address`` and their `order_total`.
    # It will calculate the customer's current rewards tier, which tier is next,
    # and their progress towards the next rewards tier and either create or update
    # the `rewards_data` for the associated `email_address`
    @coroutine
    def post(self):
        email = self.get_body_argument("email_address")
        order_total = float(self.get_body_argument("order_total"))
        points_earned = math.floor(order_total)

        # Find an existing document in the rewards_data collection for the
        # provided email, if it exists. If the document exists, add the 
        # points_earned to the document's existing reward_points.
        query = {"email_address": email}
        rewards_data = self.db.rewards_data.find_one(query)
        if rewards_data == None:
            new_points_total = points_earned
        else:
            new_points_total = rewards_data["reward_points"] + points_earned

        new_tier = self.helper.find_new_tier(new_points_total)
        next_tier = self.helper.find_next_tier(new_points_total)
        next_tier_progress = self.helper.calculate_next_tier_progress(new_points_total, new_tier["points"], next_tier["points"])

        new_values = { "$set": {
            "email_address": email,
            "reward_points": new_points_total,
            "reward_tier": new_tier["tier"],
            "reward_tier_name": new_tier["rewardName"],
            "next_reward_tier": next_tier["tier"],
            "next_reward_tier_name": next_tier["rewardName"],
            "next_reward_tier_progress": next_tier_progress
        }}
        self.db.rewards_data.update_one(query, new_values, upsert=True)


