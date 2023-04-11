import pymongo

import json

from pymongo.errors import PyMongoError
from tornado.web import RequestHandler, HTTPError
from tornado.gen import coroutine

"""
Below Mongo client code should be in a DAO but having some issue with imports in the project
"""
client = pymongo.MongoClient("mongodb", 27017)
db = client["Rewards"]
collection = db["rewards"]


class OrderHandler(RequestHandler):

    @coroutine
    def post(self):
        try:
            data = json.loads(self.request.body.decode())
            email = data.get("email")
            order_total = float(data.get("order_total"))

            # Calculate the rewards data
            customer_rewards_data = self.calculate_rewards(email, order_total)

            # Store the rewards data in MongoDB
            self.store_rewards_data(customer_rewards_data)

            # Return customer rewards data as JSON
            response_data = json.dumps(customer_rewards_data, default=str)
            self.set_header("Content-Type", "application/json")
            self.write(response_data)

        except ValueError:
            raise HTTPError(400, "Invalid order total")

        except PyMongoError:
            raise HTTPError(500, "Error storing rewards data")

    def calculate_rewards(self, email, order_total):
        """
        Calculate customer rewards by order total. This method should go into order_service.py
        :param email: customer email ID
        :param order_total: order total
        :return: customer rewards dict
        """
        # Calculate reward points based on order total
        reward_points = int(order_total)

        # Find the customer's current reward tier
        reward_tier = None
        reward_tier_name = None
        for reward in collection.find().sort("points"):
            if reward["points"] <= reward_points:
                reward_tier = reward["tier"]
                reward_tier_name = reward["rewardName"]
            else:
                break

        # Find the next reward tier
        next_reward_tier = None
        next_reward_tier_name = None
        next_reward_tier_points = None
        next_reward_tier_progress = None
        for reward in collection.find().sort("points"):
            if reward_tier is not None and reward["points"] > reward_points:
                next_reward_tier = reward["tier"]
                next_reward_tier_name = reward["rewardName"]
                next_reward_tier_points = reward["points"]
                if next_reward_tier_points - reward["points"] is not 0:
                    next_reward_tier_progress = (next_reward_tier_points - reward_points) / (
                            next_reward_tier_points - reward["points"])
                else:
                    next_reward_tier_progress = (next_reward_tier_points - reward_points)
                break
            elif reward_tier is None:
                next_reward_tier = reward["tier"]
                next_reward_tier_name = reward["rewardName"]
                next_reward_tier_points = reward["points"]
                next_reward_tier_progress = (next_reward_tier_points - reward_points) / (next_reward_tier_points - 0)
                break

        # Store customer rewards data in MongoDB
        customer_rewards_data = {
            "email": email,
            "rewardPoints": reward_points,
            "rewardTier": reward_tier,
            "rewardTierName": reward_tier_name,
            "nextRewardTier": next_reward_tier,
            "nextRewardTierName": next_reward_tier_name,
            "nextRewardTierProgress": next_reward_tier_progress
        }
        return customer_rewards_data

    def store_rewards_data(self, rewards_data):
        """
        store customer rewards data in mongodb
        :param rewards_data: Customer rewards data
        :return: None
        """
        customer_db = client["CustomerData"]
        customer_db.customerdata.insert(rewards_data)
