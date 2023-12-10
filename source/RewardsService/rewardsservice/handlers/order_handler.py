from decimal import Decimal
import math
from tornado import web, escape

from pymongo import MongoClient
from tornado.gen import coroutine

CLIENT = MongoClient("mongodb", 27017)

class OrderHandler(web.RequestHandler):  
    #post method to handle new orders  
    @coroutine 
    def post(self):
        db = CLIENT["Rewards"]
        users = db["users"]
        body = escape.json_decode(self.request.body)
        customer_email = body["data"]["customer_email"]
        order_total = body["data"]["order_total"]
        order = {
            "email_address": customer_email, 
            "order_total": order_total
        }
        rewards_data = self.rewards_calculation(order)
        users.insert_one(rewards_data)
        self.write("new reward data added")

    #helper function to calculate rewards & build reward data entry
    def rewards_calculation(self, order):
        db = CLIENT["Rewards"]
        order_total = int(Decimal(order["order_total"]))
        #catch when order is $1000
        if(order_total >= 1000):
            max_reward_item = db.rewards.find_one({"points": 1000})
            max_rewards_data = {
                "_id": len(list(db.users.find())) + 1,
                "email_address": order["email_address"], 
                "reward_points": 1000, 
                "reward_tier": max_reward_item["tier"], 
                "reward_tier_name": max_reward_item["rewardName"], 
                "next_reward_tier": None, 
                "next_reward_tier_name": None, 
                "next_reward_tier_progress": None
            }
            return max_rewards_data
        #catch when order is less than $100
        if(order_total < 100):
            min_reward_item = db.rewards.find_one({"points": 100})
            min_rewards_data = {
                "_id": len(list(db.users.find())) + 1,
                "email_address": order["email_address"], 
                "reward_points": order_total,
                "reward_tier": None, 
                "reward_tier_name": None, 
                "next_reward_tier": min_reward_item["tier"], 
                "next_reward_tier_name": min_reward_item["rewardName"], 
                "next_reward_tier_progress": self.percent_to_next_tier(order_total, min_reward_item["points"])
            }
            return min_rewards_data
        #for orders less than $1000
        current_reward_item = db.rewards.find_one({"points": self.round_down(order_total)})
        next_reward_item = db.rewards.find_one({"points": current_reward_item["points"]+100})
        rewards_data = {
            "_id": len(list(db.users.find())) + 1,
            "email_address": order["email_address"], 
            "reward_points": order_total, 
            "reward_tier": current_reward_item["tier"], 
            "reward_tier_name": current_reward_item["rewardName"], 
            "next_reward_tier": next_reward_item["tier"], 
            "next_reward_tier_name": next_reward_item["rewardName"], 
            "next_reward_tier_progress": self.percent_to_next_tier(order_total, next_reward_item["points"])
        }
        return rewards_data

    #helper function to round down to nearest 100 for current reward tier
    def round_down(self, num): 
        rounded_number = math.floor(num/100) * 100 
        return rounded_number 
    
    #helper function to get percentage for next reward tier progress as decimal
    def percent_to_next_tier(self, current_num, next_num):
        percent = (next_num - current_num)/100
        return percent