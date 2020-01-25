import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))


class OrderDatatHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        email_address = self.get_argument("email_address")
        order_total = self.get_argument("order_total")
        points = order_total * 1
        for i in range(len(rewards)):
            max = int(rewards[i]['points'])
            min = int(rewards[i]['points']-100)
            if int(order_total) in range(min, max):
                current_reward = int(
                    rewards[i]['rewardName'].split()[0].strip("%"))
                next_reward = int(
                    rewards[i+1]['rewardName'].split()[0].strip("%"))
                next_reward_progress = next_reward - current_reward
                rewards_data = [
                    {'emailAddress': email_address,
                     'rewardPoints': points,
                     'rewardTier': rewards[i]['tier'],
                     'rewardTierName': rewards[i]['rewardName'],
                     'nextRewardTier': rewards[i+1]['tier'],
                     'nextRewardTierName': rewards[i+1]['rewardName'],
                     'nextRewardTierProgress': next_reward_progress/100,
                     }
                ]
                break
        db.rewards_data.insert_many(rewards_data)
