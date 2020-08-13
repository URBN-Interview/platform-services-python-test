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
    def get(self):
        # handles errors for foregin email and orderTotal input 
        self.write('<html><body><form action="/set" method="POST">'
        '<label for="email">Enter your email: </label>'
            '<input type="email" name="email"> '
        '<label for="orderTotal">Enter your Order Total: </label>'
            '<input type="number" min="0.01" step="0.01" name="orderTotal"> '
            '<input type="submit" value="Submit">'
            '</form></body></html>')


    def post(self):
        self.set_header("Content-Type", "application/json") 

        client = MongoClient("mongodb", 27017)
        rewards_db = client["Rewards"]
        db = client['Customers']

        email = self.get_body_argument('email', None)
        orderTotal = self.get_body_argument('orderTotal', None)
        rewardPoints = self.convertToInt(float(orderTotal))

        old_customer = db.Customers.find_one({'Email Address': email}, {'_id': 0})
        new_rewardPoints = 0
        # Check for unique users
        if not old_customer:
            # insert new customers into the data base
            db.Customers.insert(
            {'Email Address': email, 'Reward Points': rewardPoints})
            self.write(self.get_body_argument("email") + "  Welcome to the rewards program  ")
            
        else:
            self.write(self.get_body_argument("email") + "  Your reward points have been updated  ")
            new_rewardPoints = old_customer['Reward Points'] + rewardPoints 
            if new_rewardPoints > 1000:
                new_rewardPoints = 1000
            self.write(json.dumps(new_rewardPoints) + "\n")
            current_tier = self.getTier(new_rewardPoints)
            nextTier = self.getNextTier(current_tier)
  
            reward_tier_name = rewards_db.rewards.find_one({'tier': current_tier}, {'_id': 0})['rewardName']
            next_reward_tier_name = rewards_db.rewards.find_one({'tier': nextTier}, {'_id': 0})['rewardName']
            max_current_tier_points = rewards_db.rewards.find_one({'tier': current_tier}, {'_id': 0})['points']
            percentage_to_next_tier = 1-(new_rewardPoints)/max_current_tier_points
 
            db.Customers.update({'Email Address': email},{
                'Email Address': email,
                'Reward Points': new_rewardPoints,
                'Reward Tier': current_tier,
                'Reward Tier Name': reward_tier_name,
                'Next Reward Tier': nextTier,
                'Next Reward Tier Name': next_reward_tier_name,
                'Next Reward Tier Progress': percentage_to_next_tier})