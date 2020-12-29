import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class CustomerOrderHandler(tornado.web.RequestHandler):
    @coroutine
    #accepts order data - email address and order total - create new table/collection? 
    def post(self):
        client = MongoClient("mongodb", 27017)
        customers = client["Customers"]
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        customerReward = None
        nextTier = None
       

    #post email and order total
        #set email and orderTotal to user inputs
        email = self.get_argument('email')
        orderTotal = self.get_argument('orderTotal')

        #calc the rewardspoints based off orderTotal - aka round the total to the nearest int
        rewardsPoints = int(orderTotal)


    #calculates rewards tier if less than 1000 points
        if(rewardsPoints < 1000):
            for rewardTier in rewards:
                if(rewardsPoints>=rewardTier["points"]):
                    customerReward = rewardTier     
    #if user has less than 100 points then they do not qualify for rewards    
            if(rewardsPoints < 100):
                customerReward = {'rewardName' : 'No reward available', 'tier' : 'Not Enough Rewards Points Accumulated'}
        
        #creating customerOrder to store data
        customerOrder = {
            'email': email, 
            'points': rewardsPoints, 
            'rewardName': customerReward['rewardName'], 
            'tier': customerReward['tier']
            }
        
        #adding customerOrder data to customers collection
        customers.insert_one(customerOrder)
        
    
