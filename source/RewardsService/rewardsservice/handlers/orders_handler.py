import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class OrdersHandler():

    @coroutine
    def post(self, keys):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]             

        email = self.get_argument("email")
        amount = self.get_argument("amount")

        orders = db["Orders"]
        order = {"email": email, "amount": amount}
        orders.insert_one(order)
        
        customersOrders = list(orders.find({"email": email}))        
        totalAmount = 0
        for order in customersOrders:
            totalAmount += order.get("amount")

        assert totalAmount > 0 : "Amount must be a positive value!"
        curr_reward = db.rewards.find_one({"tier": self.currReward(totalAmount)})
        next_reward = db.rewards.find_one({"tier": self.nextReward(totalAmount)})

        progress = ""
        points = int(totalAmount)
        pointsString = str(points)
        if len(pointsString) > 2:
            progress = pointsString[1:] + "%"
        else:
            progress = pointsString + "%"

        if totalAmount >= 1000:
            customer =  {"email": email, "rewardPoints": int(totalAmount), "rewardTier": curr_reward.get("tier"), "rewardTierName": curr_reward.get("rewardName"), "nextRewardTier": "", "nextRewardTierName": "", "nextRewardTierProgress": ""}
        elif totalAmount < 100:
            customer =  {"email": email, "rewardPoints": int(totalAmount), "rewardTier": "", "rewardTierName": "", "nextRewardTier": next_reward.get("tier"), "nextRewardTierName": next_reward.get("rewardName"), "nextRewardTierProgress": progress}
        else:
            customer =  {"email": email, "rewardPoints": int(totalAmount), "rewardTier": curr_reward.get("tier"), "rewardTierName": curr_reward.get("rewardName"), "nextRewardTier": next_reward.get("tier"), "nextRewardTierName": next_reward.get("rewardName"), "nextRewardTierProgress": progress}

        customers = db["Customers"]
        customerLookup = customers.find_one(query)
        if customerLookup is None:
            customers.insert_one(customer)
        else:
            newValues = {"$set": customer}
            customers.update_one({"_id": customerLookup.get("_id")}, newValues) 
    

    def currReward(self, total):
        assert totalSpent > 0: "Earn points toward rewards every time you shop!" 
        
        if (totalSpent < 100):
            return ""
        if (totalSpent < 200):
            return "A"
        if (totalSpent < 300):
            return "B"
        if (totalSpent < 400):
            return "C"
        if (totalSpent < 500):
            return "D"
        if (totalSpent < 600):
            return "E"
        if (totalSpent < 700):
            return "F"
        if (totalSpent < 800):
            return "G"
        if (totalSpent < 900):
            return "H"
        return "J"

    def nextReward(self, total):
        curr_reward = currReward(total)
        if (curr_reward == "J"):
            return "NO BETTER REWARD!"
        ## increment the value to obtain next reward
        return chr(ord(curr_reward) + 1)
