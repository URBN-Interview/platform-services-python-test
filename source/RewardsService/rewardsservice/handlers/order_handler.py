import json	
import tornado.web	
import math	

from pymongo import MongoClient	
from pymongo import MongoClient	
from tornado.gen import coroutine	
from tornado.options import options	
from model.customer import Customers	

class OrderHandler(tornado.web.RequestHandler):	

    @coroutine	
    def post(self):	
        client = MongoClient(options.mongodb_host)	
        customerDb = client["Customers"]	
        rewardsDb = client["Rewards"]	

        email = self.get_argument('email', '')	
        orderTotal = self.get_argument('orderTotal', '')	

        oldCustomer = customerDb.customers.find_one({"email": email}, {'_id':0})	

        dollar = int(orderTotal)	

        if(oldCustomer):	
            dollar += oldCustomer['points']	
        customer = Customers(email, int(orderTotal))	
        print(customer)	

        for reward in list(rewardsDb.rewards.find({}, {"_id": 0})):	
            if(dollar < reward["points"]):	
                    nextReward = reward	
                    break	
            currentReward = reward	

        if(currentReward):	
            customer.currentReward(currentReward["tier"], currentReward['rewardName'], currentReward['points'])	
	
        if(nextReward):		
            customer.newReward(nextReward["tier"], nextReward["rewardName"], 'progress')		
            currentPoints = 0	
            if(currentReward):	
                currentPoints = currentReward['points']	
            customer.progress = currentPoints/nextReward['points']	
	
        if(oldCustomer):	
            customerDb.customers.update({'email': customer.email},	
            {'email': customer.email, 'points': dollar, 'tier': customer.tier, 'rewardName': customer.rewardName, 'nextTier': customer.nextTier, 'nextReward': customer.nextReward, 'progress': customer.progress})	
        else:	
            customerDb.customers.insert({'email': customer.email, 'points': dollar, 'tier': customer.tier, 'rewardName': customer.rewardName, 'nextTier': customer.nextTier, 'nextReward': customer.nextReward, 'progress': customer.progress})	

        result = list(customerDb.customers.find({"email": email}, {"_id": 0}))	
        self.write(json.dumps(result))	
