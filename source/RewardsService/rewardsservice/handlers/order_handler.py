from decimal import Decimal
import math
import json
from tornado import web, escape

from pymongo import MongoClient
from tornado.gen import coroutine

CLIENT = MongoClient("mongodb", 27017)

class OrderHandler(web.RequestHandler):    
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


    def rewards_calculation(self, order):
        #catch when order is $1000
        db = CLIENT["Rewards"]
        order_total = int(Decimal(order["order_total"]))
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


    def round_down(self, num): 
        rounded_number = math.floor(num/100) * 100 
        return rounded_number 
    

    def percent_to_next_tier(self, current_num, next_num):
        percent = (next_num - current_num)/100
        return percent