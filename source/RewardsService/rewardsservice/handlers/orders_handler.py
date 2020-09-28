import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class OrdersHandler():

    @coroutine
    def post(self, keys):
        client = MongoClient("mongodb", 27017)
        db = client["Customer"]

        email = self.__getattribute__("email","")
        orderTotal = self.__getattribute__("orderTotal","")
        
        reward_tier = self.rewardTier(orderTotal)
        reward_tier_name = self.rewardTierName(reward_tier)
        
        next_reward_tier = self.nextRewardTierName(reward_tier_name)
        next_reward_tier_name = self.nextRewardTierName(next_reward_tier)
        next_reward_points = self.nextRewardPoints(next_reward_tier)

        points = int(float(orderTotal))

        if (next_reward_points == "N/A"):
            progress = "N/A"
        else:
            progress - round(float(orderTotal) / next_reward_points, 2)
        customerData = {"Email Address": email, "Reward Points": points, "Reward Tier": reward_tier, "Reward Tier Name": reward_tier_name, 
            "Next Reward Tier": next_reward_tier, "Next Reward Tier Name": next_reward_tier_name, "Next Reward Tier Progress": progress}
        db.customers.insert(customerData)
        
    def rewardTier(self, totalSpent):
        if (totalSpent < 100):
            return "N/A"
        elif (totalSpent < 200):
            return "A"
        elif (totalSpent < 300):
            return "B"
        elif (totalSpent < 400):
            return "C"
        elif (totalSpent < 500):
            return "D"
        elif (totalSpent < 600):
            return "E"
        elif (totalSpent < 700):
            return "F"
        elif (totalSpent < 800):
            return "G"
        elif (totalSpent < 900):
            return "H"
        elif (totalSpent < 1000):
            return "I"
        else:
            return "J"

    def rewardTierName(self, reward_tier):        
        if (reward_tier == "N/A"):
            return "N/A"
        for map in self.maps:
            if (map["tier"] == reward_tier):
                return map["rewardName"]

    def nextRewardTier(self, reward_tier):
        if (reward_tier == "N/A"):
            return "A"
        elif (reward_tier == "J"):
            return "N/A"
        ## increment the value to obtain next reward
        else:
            return chr(ord(reward_tier) + 1)

    def nextRewardTierName(self, next_reward_tier):
        if (next_reward_tier == "N/A"):
            return "N/A"
        for map in self.maps:
            if (map["tier"] == next_reward_tier):
                return map["rewardName"]
        return "Invalid entry ..."

    
    def nextRewardPoints(self, next_reward_tier):
        if (next_reward_tier == "N/A"):
            return "N/A"
        for map in self.maps:
            if (map["tier"] == next_reward_tier):
                return map["points"]
        return "Invalid entry ..."

    maps = [
        { "tier": "A", "rewardName": "5% off purchase", "points": 100 },
        { "tier": "B", "rewardName": "10% off purchase", "points": 200 },
        { "tier": "C", "rewardName": "15% off purchase", "points": 300 },
        { "tier": "D", "rewardName": "20% off purchase", "points": 400 },
        { "tier": "E", "rewardName": "25% off purchase", "points": 500 },
        { "tier": "F", "rewardName": "30% off purchase", "points": 600 },
        { "tier": "G", "rewardName": "35% off purchase", "points": 700 },
        { "tier": "H", "rewardName": "40% off purchase", "points": 800 },
        { "tier": "I", "rewardName": "45% off purchase", "points": 900 },
        { "tier": "J", "rewardName": "50% off purchase", "points": 1000 }
    ]