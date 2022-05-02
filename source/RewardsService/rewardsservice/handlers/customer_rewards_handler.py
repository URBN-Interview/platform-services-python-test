import math
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

MIN_TIER = 100
MAX_TIER = 1000


class SingleCustomerHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self, email_address):
        db = self.settings["db"]
        customer = db.customer_rewards.find_one(
            {"emailAddress": email_address}, {"_id": 0})
        if customer is not None:
            self.write(json.dumps(customer))
        else:
            self.set_status(404)
            self.write(json.dumps(
                {"message": "rewards not found for {0}".format(email_address)}))


class CustomerRewardsHandler(tornado.web.RequestHandler):
    @ coroutine
    def get(self):
        db = self.settings["db"]
        rewards = list(db.customer_rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))

    @ coroutine
    def post(self):
        body = tornado.escape.json_decode(self.request.body)
        try:
            email_address = body["emailAddress"]
            order_total = float(body["orderTotal"])
        except KeyError:
            self.set_status(400)
            self.write(json.dumps(
                {"message": "Invalid Request. 'emailAddress' and 'orderTotal' required"}))
            return
        except ValueError:
            self.set_status(400)
            self.write(json.dumps(
                {"message": "Invalid Request. 'emailAddress' must be a string and 'orderTotal' must be a number"}))
            return
        db = self.settings["db"]
        customer_rewards = db.customer_rewards.find_one(
            {"emailAddress": email_address}, {"_id": 0}
        )
        # if none are found, create one, should move to separate findOrCreate function
        if customer_rewards is None:
            customer_rewards = {
                "emailAddress": email_address,
                "rewardsPoints": 0,
                # keep track of total. if someone spends 10.80 then 9.2, should be 20, not 19 points
                "totalSpent": 0.0,  # best way to store dollar amount in mongo?
                "rewardTier": "",
                "rewardTierName": "",
                "nextRewardTier": "",
                "nextRewardTierName": "",
                "nextRewardTierProgress": 0.0
            }
        # based on the new order value, update the rewards data
        self.updateRewards(customer_rewards, float(body["orderTotal"]))
        db.customer_rewards.replace_one(
            {"emailAddress": email_address}, customer_rewards, True)
        self.write(json.dumps(customer_rewards))

    def updateRewards(self, customer_rewards, order_total):
        db = self.settings["db"]
        updated_total = customer_rewards["totalSpent"] + order_total
        updated_points = int(updated_total)
        point_tier = self.roundDownToHundreds(updated_points)
        reward_tier = None
        next_reward_tier = None
        # check if at max tier
        reward_tier = db.rewards.find_one({"points": point_tier + 100})
        customer_rewards["rewardsPoints"] = updated_points
        customer_rewards["totalSpent"] = updated_total
        if point_tier >= MAX_TIER:
            reward_tier = db.rewards.find_one({"points": MAX_TIER})
            customer_rewards["rewardTier"] = reward_tier["tier"]
            customer_rewards["rewardTierName"] = reward_tier["rewardName"]
            customer_rewards["nextRewardTier"] = ""
            customer_rewards["nextRewardTierName"] = ""
            customer_rewards["nextRewardTierProgress"] = 0.0
        elif point_tier < MIN_TIER:
            next_reward_tier = db.rewards.find_one({"points": MIN_TIER})
            customer_rewards["rewardTier"] = ""
            customer_rewards["rewardTierName"] = ""
            customer_rewards["nextRewardTier"] = next_reward_tier["tier"]
            customer_rewards["nextRewardTierName"] = next_reward_tier["rewardName"]
            customer_rewards["nextRewardTierProgress"] = self.calcProgress(
                updated_points)
        else:
            next_reward_tier = db.rewards.find_one({"points": point_tier})
            customer_rewards["rewardTier"] = reward_tier["tier"]
            customer_rewards["rewardTierName"] = reward_tier["rewardName"]
            customer_rewards["nextRewardTier"] = next_reward_tier["tier"]
            customer_rewards["nextRewardTierName"] = next_reward_tier["rewardName"]
            customer_rewards["nextRewardTierProgress"] = self.calcProgress(
                updated_points)

    def roundDownToHundreds(self, points):
        return math.floor(points / 100) * 100

    def calcProgress(self, points):
        return 0.0 if points >= MAX_TIER else points % 100
