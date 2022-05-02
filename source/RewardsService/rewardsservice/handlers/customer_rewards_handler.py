import math
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

MIN_TIER = 100
MAX_TIER = 1000


class CustomerRewardsHandler(tornado.web.RequestHandler):

    # TODO("Implement. if email address provided, then return single, otherwise return all")
    # won't paginate due to time, but in real life should
    @coroutine
    def get(self, email_address):
        client = MongoClient("mongodb", 27017)
        db = client["CustomerRewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))

    # * **Endpoint 1:**
    #     * Accept a customer's order data: **email adress**  (ex. "customer01@gmail.com") and **order total** (ex. 100.80).
    #     * Calculate and store the following customer rewards data into MongoDB. For each dollar a customer spends, the customer will earn 1 reward point. For example, an order of $100.80 earns 100 points. Once a customer has reached the top rewards tier, there are no more rewards the customer can earn.
    #         * **Email Address:** the customer's email address (ex. "customer01@gmail.com")
    #         * **Reward Points:** the customer's rewards points (ex. 100)
    #         * **Reward Tier:** the rewards tier the customer has reached (ex. "A")
    #         * **Reward Tier Name:** the name of the rewards tier (ex. "5% off purchase")
    #         * **Next Reward Tier:** the next rewards tier the customer can reach (ex. "B")
    #         * **Next Reward Tier Name:** the name of next rewards tier (ex. "10% off purchase")
    #         * **Next Reward Tier Progress:** the percentage the customer is away from reaching the next rewards tier (ex. 0.5)
    # {
    #     "email_address": "string",
    #     "rewards_points": "number",
    #     "reward_tier": "string",
    #     "reward_tier_name": "string",
    #     "next_reward_tier": "string",
    #     "next_reward_tier_name": "string",
    #     "next_reward_tier_progress": "number"
    # }
    @coroutine
    def post(self):
        body = self.request.body
        # check for email and order_total
        # Initialize in `initialize` block
        client = MongoClient("mongodb", 27017)
        rewards_db = client["Rewards"]
        customer_db = client["CustomerRewards"]
        customer_rewards = customer_db.find_one(
            {"emailAddress": body["email_address"]}
        )
        # if none are found, create one, should move to separate findOrCreate function
        if customer_rewards is None:
            customer_rewards = {
                "emailAddress": body["email_address"],
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
        updateRewards(customer_rewards, body["order_total"])
        # TODO("save to DB")
        
        self.write(json.dumps(customer_rewards))

    # should probably be a coroutine
    def updateRewards(customer_rewards, order_total):
        client = MongoClient("mongodb", 27017)
        rewards_db = client["Rewards"]
        updated_total = customer_rewards["totalSpent"] + order_total
        updated_points = int(updated_total)
        point_tier = roundDownToHundreds(updated_points)
        reward_tier = None
        next_reward_tier = None
        # check if at max tier
        if point_tier >= MAX_TIER:
            reward_tier = rewards_db.find_one({"points": MAX_TIER})
        elif point_tier < MIN_TIER:
            next_reward_tier = rewards_db.find_one({"points": point_tier})
        else:
            reward_tier = rewards_db.find_one({"points": point_tier + 100})
        customer_rewards["rewardsPoints"] = updated_points
        customer_rewards["totalSpent"] = updated_total
        customer_rewards["rewardTier"] = reward_tier["tier"]
        customer_rewards["rewardTierName"] = reward_tier["tierNaeme"]
        customer_rewards["nextRewardTier"] = next_reward_tier["tier"]
        customer_rewards["nextRewardTierName"] = next_reward_tier["tierName"]
        customer_rewards["nextRewardTierProgress"] = calcProgress(point_tier)

    def roundDownToHundreds(points):
        return math.floor(points / 100) * 100

    def calcProgress(point_tier):
        return 0.0 if point_tier >= MAX_TIER else point_tier % 100
