import json
from abc import ABC

import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class ordersHandler(tornado.web.RequestHandler, ABC):

    @coroutine
    def post(self):
        """setting arguments that the user will enter in the url"""
        email = self.get_argument("email", "")
        orders = self.get_argument("orders", "")
        totalPoints = float(orders)

        c = Customers(email,totalPoints)
        data = list(c.db_customers.customers.find({"email": email}, {"_id": 0}))
        print(self.write(json.dumps(data)))

    get = post

"""
    Created a customer class that deals with adding and updating customers in the database
"""
class Customers:
    """initalizing mongodb data"""
    curr_reward = None
    next_reward = None
    nextTierProgress = None
    email = None
    totalPoints = 0
    customer = None

    def __init__(self, email, totalPoints):
        self.client = MongoClient("mongodb", 27017)
        self.db_rewards = self.client["Rewards"]
        self.db_customers = self.client["Customers"]
        self.email = email
        self.totalPoints = totalPoints
        self.customer = self.db_customers.customers.find_one({"email": self.email}, {"_id": 0})
        self.run()

    """Helper methods"""
    def Exist(self):
        if self.customer:
            self.totalPoints += self.customer["points"]
            return True
        else:
            return False

    """Adds customer data to the database"""
    def addCustomer(self):
        self.db_customers.customers.insert(
            {
                "email": self.email,
                "points": int(self.totalPoints),
                "rewardsTier": self.curr_reward["tier"],
                "rewardName": self.curr_reward["rewardName"],
                "nextTier": self.next_reward["tier"],
                "nextRewardName": self.next_reward["rewardName"],
                "nextTierProgress": str(self.nextTierProgress) + "%"
            }
        )

    """Updates the customers details if the customer exists"""
    def updateCustomer(self):
        self.db_customers.customers.update({"email": self.email},
                                      {
                                          "email": self.email,
                                          "points": int(self.totalPoints),
                                          "rewardsTier": self.curr_reward["tier"],
                                          "rewardName": self.curr_reward["rewardName"],
                                          "nextTier": self.next_reward["tier"],
                                          "nextRewardName": self.next_reward["rewardName"],
                                          "nextTierProgress": str(self.nextTierProgress) + "%"
                                      }
                                      )

    """Calculates the rewards for that customer"""
    def setReward(self):
        rewards = list(self.db_rewards.rewards.find({}, {"_id": 0}))
        self.nextTierProgress = 100 - self.totalPoints % 100

        if self.totalPoints >= 1000:
            self.curr_reward = rewards[-1]
            self.next_reward = {"tier": "N/A","rewardName": "N/A"}
        elif self.totalPoints < 100:
            self.curr_reward = {"tier": "N/A","rewardName": "N/A"}
            self.next_reward = rewards[0]
        else:
            idx = int(self.totalPoints / 100) % 10
            print(idx)
            self.curr_reward = rewards[idx - 1]
            self.next_reward = rewards[idx]

    """Calls the helper method to update or add the customer in the database"""
    def run(self):
        if self.Exist():
            self.setReward()
            self.updateCustomer()
        else:
            self.setReward()
            self.addCustomer()