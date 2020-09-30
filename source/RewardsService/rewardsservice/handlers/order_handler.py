import json	
import tornado.web	
import math	

from pymongo import MongoClient	
from tornado.gen import coroutine	
from tornado.options import options	

class OrderHandler(tornado.web.RequestHandler):	

    @coroutine	
    def post(self):	
        client = MongoClient(options.mongodb_host)	
        db = client["Customers"]	
        rewardsDb = client["Rewards"]	

        email = self.get_argument('email', '')	
        orderTot = self.get_argument('orderTotal', '')
        points = orderTot

        existingCust = db.customers.find_one({"email": email}, {'_id':0})		

        #if this customer already exists in the database, the total points should be their existing points + the points from this order
        if(existingCust):	
            points += existingCust['points']	

        cust = Customer(email, orderTot)	

        #see if customer is eligible for reward
        for r in rewardsDb.rewards.find({}, {"_id": 0}):	
            if(points < r["points"]):	
                nextReward = r
                break	
            curReward = r

        if (curReward):	
            cust.currentReward(
                curReward["tier"], 
                curReward['rewardName'], 
                curReward['points']
            )	
	
        if(nextReward):		
            cust.newReward(
                nextReward["tier"], 
                nextReward["rewardName"], 
                curReward["points"]/nextReward["points"]
            )		
	
        if(existingCust):	
            db.customers.update(
                {'email': cust.email},	
                {'points': points}
            )	
        else:	
            db.customers.insert(
                {'email': cust.email, 
                'points': points, 
                'tier': cust.tier, 
                'rewardName': cust.rewardName, 
                'nextTier': cust.nextTier, 
                'nextReward': cust.nextReward, 
                'progress': cust.progress}
            )	

        result = db.customers.find({"email": email}, {"_id": 0})
        self.write(json.dumps(result))	


class Customer:	
    def __init__(self, email, orderTotal):	
        self.email = email	
        self.orderTotal = orderTotal	
        self.rewardName = ""	
        self.tier = 0
        self.points = 0.0
        self.nextReward = 0.0	
        self.nextTier = ""	
        self.progress = 0.0	

    def currentReward(self, tier, name, points):	
        self.tier = tier	
        self.rewardName = name	
        self.points = points	

    def newReward(self, tier, name, progress):	
        self.tier = tier	
        self.rewardName = name	
        self.progress = progress
