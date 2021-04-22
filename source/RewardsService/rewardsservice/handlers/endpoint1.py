import json
import tornado.web
import math

from pymongo import MongoClient
from tornado.gen import coroutine

# accept customer email and order total
class Endpoint1(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        # get all rewards
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
    
    def post(self, email, order_total):
        client = MongoClient("mongodb", 27017)
        db = client["Users"]

        # grab all rewards
        db2 = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))

        # if user doesnt not exist in db continue with below

        # user = email
        # prev_reward_points = 
        reward_points = math.floor(order_total)
        for reward in rewards:
            if reward['points'] < reward_points:
                continue
            elif reward['points'] > reward_points and reward['points'] == 100:
                reward_tier = 'N/A'
                reward_tier_name = 'N/A'
                next_reward_tier = reward['tier']
                next_reward_tier_name = reward['rewardName']
                next_reward_tier_progress = reward_points/100
            elif reward['points'] > reward_points:
                break
                reward_index = rewards.index(reward)
                next_reward_tier = reward['tier']
                next_reward_tier_name = reward['rewardName']
                next_reward_tier_progress = reward_points/reward['points']
                reward_index = reward_index - 1
                for reward in rewards:
                    if rewards.index(reward) == reward_index:
                        break
                        reward_tier = reward['tier']
                        reward_tier_name = reward['rewardName']

        # for reward in rewards:
        #     reward_index = rewards.index(reward)
        #     if reward['points'] < reward_points:
        #     # if reward['points'] >= reward_points and reward['points']
        #         break
        #         reward_tier = reward['tier']
        #         reward_name = reward['rewardName']
        

        # insert info at end
        db.users.insert({
            "user": email, 
            "rewardPoints": reward_points, 
            "rewardTier": reward_tier,
            "rewardTierName": reward_tier_name,
            "nextRewardTier": next_reward_tier,
            "nextRewardTierName": next_reward_tier_name,
            "nextRewardTierProgress": next_reward_tier_progress
            })
        
        # self.write(json.dumps(email))