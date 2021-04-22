import json
import tornado.web
import math

from pymongo import MongoClient
from tornado.gen import coroutine

# accept customer email and order total
class Endpoint1(tornado.web.RequestHandler):
    # def get(self):
    #     # get all rewards
    #     client = MongoClient("mongodb", 27017)
    #     db = client["Rewards"]
    #     rewards = list(db.rewards.find({}, {"_id": 0}))
    #     self.write(json.dumps(rewards))
    
    @coroutine
    def post(self, email, order_total):
        client = MongoClient("mongodb", 27017)

        # grab all users
        db = client["Users"]
        users = list(db.users.find({}, {"_id": 0}))

        # grab all rewards
        db2 = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))

        # if user list not empty
            # code goes here

        # check if user is in db, if so get their reward points total
        for user in users:
            if user['email'] == email:
                return self.write(json.dumps(user))
                user_email = user['email']
                prev_reward_points = user['rewardPoints']
                reward_points = math.floor(order_total)
                reward_total = prev_reward_points + reward_points
                existing_user(self, user_email, reward_total, rewards, users)
            # else if user doesnt exist in db continue with below
            else:
                reward_points = math.floor(order_total)
                new_user(self, email, reward_points, rewards, users)

    def new_user(self, email, reward_points, rewards, users):
        # reward_points = math.floor(order_total)
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
                # break
                reward_index = rewards.index(reward)
                return self.write(json.dumps(reward_index))
                next_reward_tier = reward['tier']
                next_reward_tier_name = reward['rewardName']
                next_reward_tier_progress = reward_points/reward['points']
                reward_index -= 1
                for reward in rewards:
                    if rewards.index(reward) == reward_index:
                        # break
                        reward_tier = reward['tier']
                        reward_tier_name = reward['rewardName']
        users.insert({
            "email": email, 
            "rewardPoints": reward_points, 
            "rewardTier": reward_tier,
            "rewardTierName": reward_tier_name,
            "nextRewardTier": next_reward_tier,
            "nextRewardTierName": next_reward_tier_name,
            "nextRewardTierProgress": next_reward_tier_progress
            })

    def existing_user(self, email, reward_points, rewards, users):
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
                # break
                reward_index = rewards.index(reward)
                return self.write(json.dumps(reward_index))
                next_reward_tier = reward['tier']
                next_reward_tier_name = reward['rewardName']
                next_reward_tier_progress = reward_points/reward['points']
                reward_index -= 1
                for reward in rewards:
                    if rewards.index(reward) == reward_index:
                        # break
                        reward_tier = reward['tier']
                        reward_tier_name = reward['rewardName']
        users.update({
            "email": email, 
            "rewardPoints": reward_points, 
            "rewardTier": reward_tier,
            "rewardTierName": reward_tier_name,
            "nextRewardTier": next_reward_tier,
            "nextRewardTierName": next_reward_tier_name,
            "nextRewardTierProgress": next_reward_tier_progress
            })