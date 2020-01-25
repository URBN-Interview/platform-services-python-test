import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))


class OrderDatatHandler(tornado.web.RequestHandler):
    """Endpoint which accepts a customers email adress, and order total, and stores
    the their rewards data based on the amount of points they have. To explain this handler,
    I will be using a customers order total/ points of 300"""
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        # Using the argument method to accept customer email & order total.
        email_address = self.get_argument("email_address")
        order_total = self.get_argument("order_total")
        # For each dollar a customer spends, the customer will earn 1 reward point.
        customer_points = order_total * 1
        # Set up a loop to iterate over rewards collection to start comparing customer points
        for i in range(len(rewards)):
            max = int(rewards[i]['points'])
            min = int(rewards[i]['points']-100)
            """If the customers_points is in the range of the current collection's points AND the
            the current collection's points minus 100, use that collectin for the next steps.
            """
            if int(customer_points) in range(min, max):
                # Used the split and strip methods to isolate the percetage number from rewardName
                current_reward = int(
                    rewards[i]['rewardName'].split()[0].strip("%"))
                next_reward = int(
                    rewards[i+1]['rewardName'].split()[0].strip("%"))
                # Next rewrd progress is the difference between the next reward and current reward
                next_reward_progress = next_reward - current_reward
                # Setting up a rewards_data collection to store the order data
                rewards_data = [
                    {'emailAddress': email_address,
                     'rewardPoints': customer_points,
                     'rewardTier': rewards[i]['tier'],
                     'rewardTierName': rewards[i]['rewardName'],
                     'nextRewardTier': rewards[i+1]['tier'],
                     'nextRewardTierName': rewards[i+1]['rewardName'],
                     'nextRewardTierProgress': next_reward_progress/100,
                     }
                ]
                break
        # Insert our rewards data collection into the rewards db
        db.rewards_data.insert_many(rewards_data)
