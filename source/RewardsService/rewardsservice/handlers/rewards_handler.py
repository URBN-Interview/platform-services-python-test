import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

def which_reward(points):
    client = MongoClient("mongodb", 27017)
    db = client["Rewards"]
    if points >= 1000:
        reward = db.rewards.find_one({"points": 1000}, {"_id": 0})
        return reward
    else:
        points = (points // 100) * 100
        reward = db.rewards.find_one({"points": points}, {"_id": 0})
        next_reward = db.rewards.find_one({"points": points + 100}, {"_id": 0})
        return reward, next_reward

class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))

class CustomerListHandler(tornado.web.RequestHandler):

    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(customers))

class CustomerHandler(tornado.web.RequestHandler):

    def get(self, email):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer = db.customers.find_one({"email": email}, {"_id": 0})
        if customer:
            self.write(json.dumps(customer))
        else:
            raise tornado.web.HTTPError(404, log_message="Customer does not exist")

    def put(self, email):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer = db.customers.find_one({"email": email}, {"_id": 0})

        response = tornado.escape.json_decode(self.request.body)
        points = int(response["order"])
        new_points = customer["points"] + points
        customer["points"] = new_points
        reward = which_reward(new_points)
        if len(reward) == 2:
            current_reward = reward[0]
            next_reward = reward[1]
        else:
            current_reward = reward
            next_reward = reward
        customer["currentReward"] = current_reward
        customer["nextReward"] = next_reward
        customer["rewardProgress"] = (new_points - customer["currentReward"]["points"]) / 100
        db.customers.update_one({"email": email}, {"$set": customer})

        updated_customer = db.customers.find_one({"email": email}, {"_id": 0})
        self.write(json.dumps(updated_customer))
