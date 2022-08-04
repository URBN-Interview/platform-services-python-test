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

    # GET rewards_data document for the specified email, if it exists.
    # If no email is provided, it will return all rewards_data.
    # Example: GET /rewards_data?email=test@test.com
    @coroutine
    def get(self):
        if self.get_argument("email", None):
            query = {"email_address": self.get_argument("email")}
            rewards_data = self.db.rewards_data.find_one(query)
        else:
            rewards_data = list(self.db.rewards_data.find({}, {"_id": 0}))
        
        self.set_status(200)
        self.write(json.dumps(rewards_data, default=lambda o: '<not serializable>'))
    
    # POST with a payload of a customer's `email_address`` and their `order_total`.
    # It will calculate the customer's current rewards tier, which tier is next,
    # and their progress towards the next rewards tier and either create or update
    # the `rewards_data` for the associated `email_address`
    # Example: POST /rewards_data, payload: { "email_address": "test@test.com", "order_total": 100}
    @coroutine
    def post(self):
        email = self.get_body_argument("email_address")
        order_total = self.get_body_argument("order_total")
        
        valid, error = self.helper.validate_input(email, order_total)
        if not valid:
            raise tornado.web.HTTPError(400, reason=error)

        points_earned = int(float(order_total))

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

        self.set_status(200)
        self.write("OK")
