import json, math
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        rewards = db.rewards.find_one({"points": 200})
        self.write(str(rewards))
        

class EndPointOne(tornado.web.RequestHandler):
    def get(self):
        self.render("endpoint_one.html", title="get")
    
    def post(self):
        client = MongoClient("mongodb", 27017)
        user_info_db = client["user_info"]
        rewards_db = client["Rewards"]
        email = self.get_argument("email")
        saved_user_info = user_info_db.user_info.find_one({"email":email})
        if saved_user_info:
            tier, points = self.calculate_points(
                int(self.get_argument("points")),
                int(saved_user_info.get('points'))
            ) 
        else:
            tier, points = self.calculate_points(int(self.get_argument("points")))
            user_info_db.user_info.insert({"email":email, "points":points})
        tier_progress = (points%100)/100
        if points< 100:
            reward = {'tier': 'None','rewardName': 'None'}
            next_reward = rewards_db.rewards.find_one( {"points": tier+100})
        elif points < 1000:
            reward = rewards_db.rewards.find_one( {"points": tier})
            next_reward = rewards_db.rewards.find_one( {"points": tier+100})   
        else:
            reward = rewards_db.rewards.find_one( {"points": tier})
            next_reward = {'tier': 'None','rewardName': 'None'}
            tier_progress = "Maxed Out"
        user_reward_dic = {
            "email" : email,
            "reward_points" : points,
            "reward_tier" : reward.get('tier'),
            "reward_tier_name" : reward.get('rewardName'),
            "next_reward_tier" : next_reward.get('tier'),
            "next_reward_tier_name" : next_reward.get('rewardName'),
            "next_reward_tier_progress" : tier_progress
            }
        self.update_user_info(user_info_db, **user_reward_dic)
        self.render("data_display.html", title="post", users=[user_reward_dic])

    def calculate_points(self,new_points, old_points=0):
        total_points = new_points+old_points
        if total_points < 100:
            return (0, total_points)
        else:
            tier = int(math.ceil(total_points / 100.0)) * 100 
            return (tier if tier <1000 else 1000, total_points)
    
    def update_user_info(
            self,
            user_info_db,
            email, 
            reward_points, 
            reward_tier, 
            reward_tier_name, 
            next_reward_tier, 
            next_reward_tier_name, 
            next_reward_tier_progress):
        user_info_db.user_info.update_one({"email":email},
        {"$set":{
            "reward_points":reward_points,
            "reward_tier":reward_tier,
            "reward_tier_name":reward_tier_name, 
            "next_reward_tier": next_reward_tier, 
            "next_reward_tier_name": next_reward_tier_name, 
            "next_reward_tier_progress": next_reward_tier_progress}}) 

class EndPointTwo(tornado.web.RequestHandler):
    """get user info"""
    def get(self):
        self.render("endpoint_two.html", title="post",)
    def post(self):
        client = MongoClient("mongodb", 27017)
        user_info_db = client["user_info"]
        email = self.get_argument("email")
        user_info = user_info_db.user_info.find_one({"email":email})
        if user_info:
            self.render("data_display.html", title="post", users=[user_info])
        else:
            self.write("that email does not exist in the database")


class EndPointThree(tornado.web.RequestHandler):
    """Get all user Info"""
    def get(self):
        client = MongoClient("mongodb", 27017)
        user_info_db = client["user_info"]
        user_info = list(user_info_db.user_info.find({}))
        self.render("data_display.html", title="post", users=user_info)