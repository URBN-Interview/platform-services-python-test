import json	
import tornado.web	
import math	

from pymongo import MongoClient	
from tornado.gen import coroutine	
from tornado.options import options	
from model.customer import Customer	

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

        cust = Customer(email, orderTot))	

        #see if customer is eligible for reward
        for r in rewardsDb.rewards.find({}, {"_id": 0}):	
            if(points < r["points"]):	
                nextReward = r
                break	
            curReward = reward	

        if (curReward):	
            cust.currentReward(
                curReward["tier"], 
                curReward['rewardName'], 
                curReward['points']
            )	
	
        if(nextReward):		
            customer.newReward(
                nextReward["tier"], 
                nextReward["rewardName"], 
                curReward["points"]/nextReward["points"]
            )		
	
        if(oldCustomer):	
            customerDb.customers.update(
                {'email': customer.email},	
                {'points': points}
            )	
        else:	
            customerDb.customers.insert(
                {'email': customer.email, 
                'points': points, 
                'tier': customer.tier, 
                'rewardName': customer.rewardName, 
                'nextTier': customer.nextTier, 
                'nextReward': customer.nextReward, 
                'progress': customer.progress}
            )	

        result = customerDb.customers.find({"email": email}, {"_id": 0})
        self.write(json.dumps(result))	
