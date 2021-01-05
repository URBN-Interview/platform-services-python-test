import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class CustomerOrderHandler(tornado.web.RequestHandler):
    @coroutine
    #accepts order data - email address and order total - create new table/collection? 
    def post(self):
        client = MongoClient("mongodb", 27017)
        
        db = client["Rewards"]
        customers = db["Customers"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        customerReward = None
        nextTier = None
       

    #post email and order total
        #set email and orderTotal to user inputs
        email = self.get_argument("email", "")
        orderTotal = self.get_argument("orderTotal", "")
        #calc the rewardspoints based off orderTotal - aka round the total to the nearest int
        rewardsPoints = int(orderTotal)


    #calculates rewards tier if less than 1000 points
        if(rewardsPoints < 1000):
            for rewardTier in rewards:
                if(rewardsPoints>=rewardTier["points"]):
                    customerReward = rewardTier
                elif(rewardsPoints < rewardTier["points"]):
                    nextTier = rewardTier   
                    break
    #if user has less than 100 points then they do not qualify for rewards    
            if(rewardsPoints < 100):
                customerReward = {"rewardName" : "No reward available", "tier" : "Not Enough Rewards Points Accumulated"}
            calculation = 100 * ( (rewardsPoints / nextTier ["points"]) )  
            nextTierProgress = str(calculation) + "%"  
       
    
        #creating customerOrder to store data
            customerOrder = {
                "email": email, 
                "points": rewardsPoints, 
                "rewardName": customerReward["rewardName"], 
                "tier": customerReward["tier"],
                "nextTier" : nextTier["tier"],
                "nextRewardName" : nextTier["rewardName"],
                "progressToNextTier" : nextTierProgress

            }
        
        #adding customerOrder data to customers collection
            customers.insert_one(customerOrder)
        
        #set variables if highest tier is reached
        else:
            customerReward = {"rewardName" : "50% off purchase", "tier" : "J"}   
            customerOrder = {
                "email": email, 
                "points": rewardsPoints, 
                "rewardName": customerReward["rewardName"], 
                "tier": customerReward["tier"],
                "nextTier" : "Reached highest tier.",
                "nextRewardName" : "Reached highest tier.",
                "progressToNextTier" : "NA"
            }

            customers.insert_one(customerOrder)

class CustomerHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customers = db["Customers"]
        email = self.get_argument("email", "")
        customer = customers.find_one({"email": email}, {"_id": 0})
        self.write(json.dumps(customer))
      
class AllCustomersHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customers = db["Customers"]
        allCustomers = list(customers.find({}, {"_id": 0}))
        self.write(json.dumps(allCustomers))