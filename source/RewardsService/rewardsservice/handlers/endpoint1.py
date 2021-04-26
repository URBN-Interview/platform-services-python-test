import json
import tornado.web
import math

from pymongo import MongoClient
from tornado.gen import coroutine

# accept customer email and order total
class Endpoint1(tornado.web.RequestHandler):
    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)

        # grab all rewards
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        
        # create user collection if its not already there
        if 'users' in db.list_collection_names():
            pass
        else:
            db.create_collection('users')

        # grab all users
        users = list(db.users.find({}, {"_id": 0}))

        # get email and order_total
        email = self.get_body_argument('email')
        order_total = self.get_body_argument('order_total')
        order_total = float(order_total)

        # check if user is in db, if so get their reward points total. else create new user
        user_emails = [user['email'] for user in users]
        if email in user_emails:
            for user in users:
                for key in user:
                    if user['email'] == email: 
                        prev_reward_points = user['rewardPoints']
                        reward_points = math.floor(order_total)
                        reward_total = prev_reward_points + reward_points
            self.existing_user(email, reward_total, rewards, users, db)
        else:
            reward_points = math.floor(order_total)
            self.new_user(email, reward_points, rewards, users, db)
    # new user -> loop through rewards and compare rewards_points to rewardPoints, return if latter is greater than former
    def new_user(self, email, reward_points, rewards, users, db):
        for reward in rewards:
            if reward['points'] < reward_points and reward_points > 1000:
                reward_tier = 'J'
                reward_tier_name = '50% off purchase'
                next_reward_tier = "N/A"
                next_reward_tier_name = "N/A"
                next_reward_tier_progress = "N/A"
                db.users.insert({
                    "email": email, 
                    "rewardPoints": reward_points, 
                    "rewardTier": reward_tier,
                    "rewardTierName": reward_tier_name,
                    "nextRewardTier": next_reward_tier,
                    "nextRewardTierName": next_reward_tier_name,
                    "nextRewardTierProgress": next_reward_tier_progress
                })
                break
            elif reward['points'] < reward_points:
                continue
            elif reward['points'] > reward_points and reward['points'] == 100: # this block works
                reward_tier = 'N/A'
                reward_tier_name = 'N/A'
                next_reward_tier = reward['tier']
                next_reward_tier_name = reward['rewardName']
                next_reward_tier_progress = reward_points/100
                next_reward_tier_progress = "{:.0%}".format(next_reward_tier_progress)
                db.users.insert({
                    "email": email, 
                    "rewardPoints": reward_points, 
                    "rewardTier": reward_tier,
                    "rewardTierName": reward_tier_name,
                    "nextRewardTier": next_reward_tier,
                    "nextRewardTierName": next_reward_tier_name,
                    "nextRewardTierProgress": next_reward_tier_progress
                })
                break
            elif reward['points'] > reward_points: # this one works
                reward_index = rewards.index(reward)
                next_reward_tier = reward['tier']
                next_reward_tier_name = reward['rewardName']
                next_reward_tier_progress = reward_points/reward['points']
                next_reward_tier_progress = "{:.0%}".format(next_reward_tier_progress)
                reward_index -= 1
                for reward in rewards:
                    if rewards.index(reward) == reward_index:
                        reward_tier = reward['tier']
                        reward_tier_name = reward['rewardName']
                        db.users.insert({
                            "email": email, 
                            "rewardPoints": reward_points, 
                            "rewardTier": reward_tier,
                            "rewardTierName": reward_tier_name,
                            "nextRewardTier": next_reward_tier,
                            "nextRewardTierName": next_reward_tier_name,
                            "nextRewardTierProgress": next_reward_tier_progress
                        })
                        break
                break
    
    # existing user code
    def existing_user(self, email, reward_points, rewards, users, db):
        for reward in rewards:
            if reward['points'] < reward_points and reward_points > 1000:
                reward_tier = 'J'
                reward_tier_name = '50% off purchase'
                next_reward_tier = "N/A"
                next_reward_tier_name = "N/A"
                next_reward_tier_progress = "N/A"
                db.users.update_one(
                    {"email": email}, 
                        {"$set": {
                            "rewardPoints": reward_points, 
                            "rewardTier": reward_tier,
                            "rewardTierName": reward_tier_name,
                            "nextRewardTier": next_reward_tier,
                            "nextRewardTierName": next_reward_tier_name,
                            "nextRewardTierProgress": next_reward_tier_progress
                        }}
                    )
                break
            elif reward['points'] < reward_points:
                continue
            elif reward['points'] > reward_points and reward['points'] == 100:
                reward_tier = 'N/A'
                reward_tier_name = 'N/A'
                next_reward_tier = reward['tier']
                next_reward_tier_name = reward['rewardName']
                next_reward_tier_progress = reward_points/100
                next_reward_tier_progress = "{:.0%}".format(next_reward_tier_progress)
                db.users.update_one(
                    {"email": email}, 
                        {"$set": {
                            "rewardPoints": reward_points, 
                            "rewardTier": reward_tier,
                            "rewardTierName": reward_tier_name,
                            "nextRewardTier": next_reward_tier,
                            "nextRewardTierName": next_reward_tier_name,
                            "nextRewardTierProgress": next_reward_tier_progress
                        }}
                    )
                break
            elif reward['points'] > reward_points:
                reward_index = rewards.index(reward)
                next_reward_tier = reward['tier']
                next_reward_tier_name = reward['rewardName']
                next_reward_tier_progress = reward_points/reward['points']
                next_reward_tier_progress = "{:.0%}".format(next_reward_tier_progress)
                reward_index -= 1
                for reward in rewards:
                    if rewards.index(reward) == reward_index:
                        reward_tier = reward['tier']
                        reward_tier_name = reward['rewardName']
                        db.users.update_one(
                            {"email": email}, 
                                {"$set": {
                                    "rewardPoints": reward_points, 
                                    "rewardTier": reward_tier,
                                    "rewardTierName": reward_tier_name,
                                    "nextRewardTier": next_reward_tier,
                                    "nextRewardTierName": next_reward_tier_name,
                                    "nextRewardTierProgress": next_reward_tier_progress
                                }}
                            )
                        break
                break
        # self.write(json.dumps(users))