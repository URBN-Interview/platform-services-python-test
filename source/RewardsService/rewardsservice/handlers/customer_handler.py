import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
import math


#following OOD design best practices, I am creating a class to handle the customer operations and rewards
class CustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self): 
        ""
        # client = MongoClient("mongodb", 27017)
        # # self.write(client.list_database_names()) 
        # db = client["Customers"]
        # email_address = self.get_argument("emailAddress", None)
        # self.write(db.customers.find_one({"emailAddress": email_address}, {"_id": 0}))
        # # if not email_exists:
        #     self.write("This email doesn't exist in the system!")
        #     #insert a new one to the database
        # else: 
        #   self.write(db.customers.find_one({"emailAddress": email_address}, {"_id": 0}))



    # gets the email addrress and order total
    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]
        email_address = self.get_argument("emailAddress", None)
        order_total = self.get_argument("orderTotal", None)
        email_address = "moretest@testing.com"
        order_total = 100

        customer_exists = db.customers.find_one({"emailAddress": email_address}, {"_id": 0})
        self.write(json.dumps(db.customers.find_one({"emailAddress": email_address}, {"_id": 0})))
        reward_points = order_total

        #if customer does not already exist
        if not customer_exists:
            #insert a new one to the database
            self.write("Email doesn't exists")
            customer_reward = self.get_customer_reward(reward_points)
            customer_reward.update({'emailAddress': email_address})
            db.customers.insert(customer_reward)
            self.write(json.dumps(db.customers.find_one({"emailAddress": email_address}, {"_id": 0})))
        else:
            #simply update 
            reward_points = float(customer_exists["rewardPoints"] + reward_points)
            customer_reward = self.get_customer_reward(reward_points)
            customer_reward.update({'emailAddress': email_address})
            db.customers.update_one({"emailAddress": email_address},
                {'$set': customer_reward})
            self.write("email exists")
            self.write(json.dumps(db.customers.find_one({"emailAddress": email_address}, {"_id": 0})))

        #function that returns the customer reward information
    def get_customer_reward(self,reward_points):
        #round down to whole number
        rounded_reward_points = math.floor(reward_points)
        #get current and next reward points - if the points are more than or equal to 1000 (tier F), there's no next reward
        if rounded_reward_points >= 1000 : current_reward_points = 1000 
        else : current_reward_points = rounded_reward_points
        
        if current_reward_points >= 1000 : next_reward_points = 1000
        else : next_reward_points = current_reward_points + 100

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        current_reward = db.rewards.find_one(
            {"points": current_reward_points},
            {"_id": 0, "points": 0})
        next_reward = db.rewards.find_one(
            {"points": next_reward_points},
            {"_id": 0, "points": 0})
        # if current reward does not exist, it means this is a new customer starting off
        if not current_reward:
            current_reward = {"tier": "0", "rewardName": "0% off purchase"}
        #this gets the decimal percent based on the example. E.g 1 - 400/500 = 0.2 
        if current_reward_points == 1000: progress = 0
        else : progress = 1 - (current_reward_points /next_reward_points)
        #return all the fields info  
        return({
            "rewardPoints": reward_points,
            "rewardTier": current_reward["tier"],
            "rewardTierName": current_reward["rewardName"],
            "nextRewardTier": next_reward["tier"],
            "nextRewardTierName": next_reward["rewardName"],
            "nextRewardTierName": progress})








