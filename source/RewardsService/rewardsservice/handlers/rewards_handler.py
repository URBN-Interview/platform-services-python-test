import json
import tornado.web

from pymongo import MongoClient, ASCENDING
from tornado.gen import coroutine

mongo_client = MongoClient("localhost", 27017)


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = mongo_client
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))



class CalculateRewardsHandler(tornado.web.RequestHandler):
    def initialize(self):
        client = mongo_client #MongoClient("mongodb", 27017)
        db = client["Rewards"]
        self.db = db

    def post(self):
        email = self.get_argument("email")
        order_total = float(self.get_argument("order_total"))

        orders = self.calculate_rewards(email, order_total)

        # Store rewards data in MongoDB
        self.db.orders.insert_one(orders)

        self.write({"success": True})

    def calculate_rewards(self, email, order_total):
        rewards_data = self.db.rewards.find().sort("points", ASCENDING)

        total_points = int(order_total)
        current_tier = None
        next_tier = None
        for reward in rewards_data:
            if total_points >= reward["points"]:
                current_tier = reward
            else:
                next_tier = reward
                break
        next_tier_name = None
        if current_tier:
            next_tier_points = next_tier["points"] if next_tier else None
            next_tier_name = next_tier["rewardName"] if next_tier else None
            next_tier_progress = (next_tier_points - total_points) / (next_tier_points - current_tier["points"])
            if next_tier_progress < 0:
                next_tier_progress = 0
        else:
            current_tier = next_tier = None
            next_tier_progress = None

        return {
            "email": email,
            "reward_points": total_points,
            "reward_tier": current_tier["tier"] if current_tier else None,
            "reward_tier_name": current_tier["rewardName"] if current_tier else None,
            "next_reward_tier": next_tier["tier"] if next_tier else None,
            "next_reward_tier_name": next_tier_name,
            "next_reward_tier_progress": next_tier_progress
        }

class RetrieveCustomerRewardsHandler(tornado.web.RequestHandler):
    def initialize(self):
        client = mongo_client #MongoClient("mongodb", 27017)
        db = client["Rewards"]
        self.db = db

    def get(self, email):
        rewards = self.db.orders.find_one({"email": email})
        if rewards:
            del rewards["_id"]
            self.write(rewards)
        else:
            self.set_status(404)
            self.write({"error": "Rewards data not found for the provided email."})

class RetrieveAllCustomersRewardsHandler(tornado.web.RequestHandler):
    def initialize(self):
        client = mongo_client #MongoClient("mongodb", 27017)
        db = client["Rewards"]
        self.db = db

    def get(self):
        orders = self.db.orders.find({}, {"_id": 0})
        # self.write(list(rewards))
        orders_list = list(orders)
        orders_json = json.dumps(orders_list)  # Convert list to JSON string
        self.write(orders_json.encode())  # Encode JSON string to bytes and write to response


