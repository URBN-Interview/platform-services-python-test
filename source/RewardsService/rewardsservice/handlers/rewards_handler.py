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
        # self.write(str(rewards['tier']))
        self.write(str(rewards))
        

class EndPointOne(tornado.web.RequestHandler):
    def get(self):
        self.render("endpoint_one.html", title="get")
    
    def post(self):
        client = MongoClient("mongodb", 27017)
        user_info_db = client["user_info"]
        rewards_db = client["Rewards"]
        email = self.get_argument("email")
        saved_user_info = user_info_db.users.find_one({"email":email})
        if saved_user_info:
            tier, points = self.calculate_points(
                int(self.get_argument("points")),
                int(saved_user_info.get('points'))
            )
            user_info_db.users.update_one({"email":email},{"$set":{"points":points}})   
        else:
            tier, points = self.calculate_points(int(self.get_argument("points")))
            user_info_db.users.insert({"email":email, "points":points})
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
            "email_address" : email,
            "reward_points" : points,
            "reward_tier" : reward.get('tier'),
            "reward_tier_name" : reward.get('rewardName'),
            "next_reward_tier" : next_reward.get('tier'),
            "next_reward_tier_name" : next_reward.get('rewardName'),
            "next_reward_tier_progress" : tier_progress
            }
        self.render("endpoint_one_post.html", title="post", spot=user_reward_dic)

    def calculate_points(self,new_points, old_points=0):
        total_points = new_points+old_points
        if total_points < 100:
            return (0, total_points)
        else:
            tier = int(math.ceil(total_points / 100.0)) * 100 
            return (tier if tier <1000 else 1000, total_points)

class EndPointTwo(tornado.web.RequestHandler):
    """get user info"""
    def get(self):
        self.write(self.__class__.__name__)

class EndPointThree(tornado.web.RequestHandler):
    """Get all user Info"""
    def get(self):
        self.write(self.__class__.__name__)