import json	
import tornado.web	
import math	

from pymongo import MongoClient	
from tornado.gen import coroutine	
from tornado.options import options	

class OrderHandler(tornado.web.RequestHandler):	

    @coroutine	
    def post(self):	
        client = MongoClient("mongodb", 27017)	
        db = client["Customers"]	
        rewardsDb = client["Rewards"].rewards

        email = self.get_argument('email', '')	
        orderTot = self.get_argument('orderTotal', '')
        tier = self.tier(orderTot)
        rewardName = self.rewardName(tier)
        nextTier = self.nextTier(rewardName)
        nextReward = self.nextReward(nextTier)
        points = int(orderTot)
        existingCust = db.customers.find_one({"email": email}, {'_id':0})		

        if(nextReward == ""):
            progress = ""
        else:
            progress = orderTot/nextReward

        if(existingCust):	
            db.customers.update(
                {'email': email},	
                {'points': points}
            )	
        else:	
            db.customers.insert(
                {'email': email, 
                'points': points, 
                'tier': tier, 
                'rewardName': rewardName, 
                'nextTier': nextTier, 
                'nextReward': nextReward, 
                'progress': progress}
            )
        
    def tier(self, spent):
        if (spent < 100):
            return "N/A"
        elif (spent < 200):
            return "A"
        elif (spent < 300):
            return "B"
        elif (spent < 400):
            return "C"
        elif (spent < 500):
            return "D"
        elif (spent < 600):
            return "E"
        elif (spent < 700):
            return "F"
        elif (spent < 800):
            return "G"
        elif (spent < 900):
            return "H"
        elif (spent < 1000):
            return "I"
        else:
            return "J"
        
    def rewardName(self, rewardName):   
        if (rewardName == "N/A"):
            return "N/A"
        for reward in rewardsDb:
            if (reward["tier"] == rewardName):
                return reward["rewardName"]

    def nextTier(self, tier):
        if (tier == ""):
            return "A"
        elif (tier == "J"):
            return ""
        else:
            return chr(ord(tier) + 1)
    
    def nextReward(self, tier):
        if (tier == ""):
            return ""
        for reward in rewardsDb:
            if (reward["tier"] == tier):
                return reward["points"]
        return ""

client = MongoClient("mongodb", 27017)	
db = client["Customers"]	
rewardsDb = client["Rewards"].rewards