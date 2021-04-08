import json
import tornado.web
import math

from pymongo import MongoClient
from tornado.gen import coroutine


class UserHandler(tornado.web.RequestHandler):

    
    def get_current_tier(self, rewards_points, db):
        #Check if customer is in the final tier
        if (rewards_points >= 1000):
            return "J"
        #Calculate points tier and search database for tier letter
        points_floor = (rewards_points - (rewards_points % 100))
        document = db.rewards.find_one({"points": points_floor})
        #null check
        if document is None:
            return None
        #Return appropriate tier letter and reward type
        current_tier = document["tier"]
        current_tier_reward = document["rewardName"]
        return current_tier, current_tier_reward

    def get_next_tier(self, rewards_points, db):
        current_tier = self.get_current_tier(rewards_points, db)
        #Check if customer is in the final tier
        if (current_tier == "J"):
            return "N/A"
        #Calculate next points tier and search database for tier letter
        points_cieling = (rewards_points + (100 - (rewards_points % 100)))
        document = db.rewards.find_one({"points": points_cieling})
        #null check
        if document is None:
            return None
        #Return appropriate tier letter and reward type
        next_tier = document["tier"]
        next_tier_reward = document["rewardName"]
        return next_tier, next_tier_reward
        
        

    def calculate_percent(self, rewards_points):
        if (rewards_points >= 1000):
            return 0
        return (rewards_points % 100) / 100

    def add_to_db(self, user_email, amount_spent, db):
        #TODO remove this next line, find better place to clear the database when new server is loaded
        db.user_info.remove()
        rewards_points = math.trunc(amount_spent)
        user_progress = self.calculate_percent(rewards_points)
        current_tier, current_tier_reward = self.get_current_tier(rewards_points, db)
        next_tier, next_tier_reward = self.get_next_tier(rewards_points, db)
        db.user_info.insert({"userEmail": user_email, "rewardPoints": rewards_points,"currentTier": current_tier, "currentReward": current_tier_reward,
                             "nextTier": next_tier, "nextReward": next_tier_reward, "progress": user_progress})
        


    #@coroutine    
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        amount_spent = float(self.get_body_argument("total"))
        user_email = self.get_body_argument("username")
        self.add_to_db(user_email, amount_spent, db)
        rewards = list(db.user_info.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))

    
    



    


        
