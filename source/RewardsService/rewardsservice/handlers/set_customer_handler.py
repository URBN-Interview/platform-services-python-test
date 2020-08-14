# set_customer_handler.py
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class SetCustomerHandler(tornado.web.RequestHandler):

    def getTier(self, points):
        if points >= 900: return "J"
        elif points >= 800: return "I"
        elif points >= 700: return "H"
        elif points >= 600: return "G"
        elif points >= 500: return "F"
        elif points >= 400: return "E"
        elif points >= 300: return "D"
        elif points >= 200: return "C"
        elif points >= 100: return "B"
        elif points >= 0: return "A"
        else : return "J"

    def getNextTier(self, myTier):
        nextTier = chr(ord(myTier) + 1)
        if nextTier > 'J':
            nextTier = 'J'
        return nextTier
    
    # Work around created because standard int() was not working 
    def convertToInt(self, float):
    # check for whole number 
        if (float % 1 != 0):
            integer = float // 1
        else:
            integer = float
        return integer


    @coroutine
    def post(self):
        self.set_header("Content-Type", "application/json") 

        client = MongoClient("mongodb", 27017)
        rewards_db = client["Rewards"]
        db = client['Customers']

        email = self.get_body_argument('emailAddress', None)
        orderTotal = self.get_body_argument('orderTotal', None)
        points = self.convertToInt(float(orderTotal))

        old_customer = db.Customers.find_one({'emailAddress': email}, {'_id': 0})
        new_rewardPoints = 0
        # Check for unique users
        if not old_customer:
            # insert new customers into the data base
            current_tier = self.getTier(points)
            nextTier = self.getNextTier(current_tier)

            reward_tier_name = rewards_db.rewards.find_one({'tier': current_tier}, {'_id': 0})['rewardName']
            next_reward_tier_name = rewards_db.rewards.find_one({'tier': nextTier}, {'_id': 0})['rewardName']
            max_current_tier_points = rewards_db.rewards.find_one({'tier': current_tier}, {'_id': 0})['points']
            percentage_to_next_tier = 1-(points)/100

            db.Customers.insert(
            {'emailAddress': email,
            'rewardPoints': points,
            'rewardTier': current_tier,
            'rewardTierName': reward_tier_name,
            'nextRewardTier': nextTier,
            'nextRewardTierName': next_reward_tier_name,
            'nextTierProgress': percentage_to_next_tier},)
            current_tier = self.getTier(new_rewardPoints)
            nextTier = self.getNextTier(current_tier)

            
        else:
            new_rewardPoints = old_customer['rewardPoints'] + points 
            if new_rewardPoints > 1000:
                new_rewardPoints = 1000

            current_tier = self.getTier(new_rewardPoints)
            nextTier = self.getNextTier(current_tier)
  
            reward_tier_name = rewards_db.rewards.find_one({'tier': current_tier}, {'_id': 0})['rewardName']
            next_reward_tier_name = rewards_db.rewards.find_one({'tier': nextTier}, {'_id': 0})['rewardName']
            max_current_tier_points = rewards_db.rewards.find_one({'tier': current_tier}, {'_id': 0})['points']
            percentage_to_next_tier = 1-(new_rewardPoints)/max_current_tier_points
 
            db.Customers.update({'emailAddress': email},{
                'emailAddress': email,
                'rewardPoints': new_rewardPoints,
                'rewardTier': current_tier,
                'rewardTierName': reward_tier_name,
                'nextRewardTier': nextTier,
                'nextRewardTierName': next_reward_tier_name,
                'nextTierProgress': percentage_to_next_tier})
        customer = db.Customers.find_one({'emailAddress': email}, {'_id':0})
        self.write(customer)