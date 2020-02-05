import json
import math

import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

# This class handles **Endpoint 2:** and **Endpoint 3:**
# url: /customers
class CustomersHandler(tornado.web.RequestHandler):

    # GET endpoint
    # request parameter: 'email-address'
    # returns: Customer information for specified 'email-address'
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]
        email_address = self.get_argument('email-address')
        customers = list(
            db.customers.find({"emailAddress": email_address}, {"_id": 0}))
        self.write(json.dumps(customers))

    # POST endpoint
    # request parameters: 'email-address', 'order-total'
    # This endpoint calculates and stores the following customer rewards data.
    @coroutine
    def post(self):
        # get mongodb
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]

        # get request parameters
        email_address = self.get_argument('email-address')
        order_total = float(self.get_argument('order-total'))

        # query for customer
        filtering = {"emailAddress": email_address}
        projection = {"_id": 0}
        customer = db.customers.find_one(filtering, projection)

        # if customer already exists, then update query must be used where we add to customer's existing reward points
        # else - insert new customer data
        if customer:
            new_order_total = float(customer["rewardPoints"] + order_total)
            filtering = {"emailAddress": email_address}
            query = {"$set": self.build_query(email_address, new_order_total)}
            db.customers.update_one(filtering, query)
        else:
            query = self.build_query(email_address, order_total)
            db.customers.insert(query)

    # input: email-address, order-total
    # returns: dictionary of the Customer data to insert/update into MongoDB
    def build_query(self, email_address, order_total):
        current_reward = self.get_reward(order_total, False)
        next_reward = self.get_reward(order_total, True)
        next_reward_progress = self.calculate_progress(order_total, next_reward["points"])
        return self.build_document(email_address, order_total,
                                   current_reward["tier"], current_reward["rewardName"],
                                   next_reward["tier"], next_reward["rewardName"], next_reward_progress)

    # input: reward_points (float) - the amount of reward points for the current transaction
    #        next_reward (boolean) - if true, get data for customer's next rewards tier.
    #                                if false, get data for customer's current rewards tier
    # returns: Rewards data (tier, tier name, and points)
    def get_reward(self, reward_points, next_reward):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        # if calculating the next reward, then round up to nearest 100
        # if calculating the current reward, then round down to nearest 100
        if next_reward:
            reward_points_rounded = self.round_up(reward_points)
        else:
            reward_points_rounded = self.round_down(reward_points)

        # if customer's reward points is less that 100, then customer has no current rewards
        # if customer's reward points is greater that 1000, then customer ha no next rewards
        if reward_points_rounded < 100 or reward_points_rounded > 1000:
            return self.no_rewards(reward_points)
        else:
            return db.rewards.find_one({"points": reward_points_rounded})

    @staticmethod
    def build_document(email_address, reward_points, reward_tier, reward_tier_name,
                       next_reward_tier, next_reward_tier_name, next_reward_tier_progress):
        return {"emailAddress": email_address, "rewardPoints": reward_points, "rewardTier": reward_tier,
                "rewardTierName": reward_tier_name, "nextRewardTier": next_reward_tier,
                "nextRewardTierName": next_reward_tier_name, "nextRewardTierProgress": next_reward_tier_progress}

    @staticmethod
    def no_rewards(points):
        return {"points": points, "rewardName": "N/A", "tier": "N/A"}

    @staticmethod
    def calculate_progress(current_points, goal):
        # if customer has over 1000 points, then there is no next reward tier to progress towards
        if current_points > 1000:
            return 0
        else:
            return goal - current_points

    @staticmethod
    def round_down(reward_points):
        return min(int(math.floor(reward_points / 100.0)) * 100, 1000)

    @staticmethod
    def round_up(reward_points):
        return int(math.ceil((reward_points + 1.0) / 100.0)) * 100
