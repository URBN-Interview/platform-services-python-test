import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
       
        # rewards
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        
        json_response = {"rewards": rewards}

        self.write(json.dumps(json_response))

    # handle customer information and commit to database
    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        json_response = {"success": True}

        # get post data
        json_request = tornado.escape.json_decode(self.request.body)

        # build customer data struct/collection entry
        points = int(json_request["total"])
        customer = {
            "email": json_request["email"],
            "points": json_request["total"],
            "tier": None,
            "tier_name": None,
            "next_tier": None,
            "next_tier_name": None,
            "next_tier_progress": 0
        }

        # get tier information from current points to next tier
        # order by points
        reward_query = db.rewards.find({
            "points": {"$gte": points}},
            {"_id": 0}).sort("points", 1).limit(2)
        rewards = list(reward_query)

        if len(rewards) == 2:
            # add reward data to customer
            customer["tier"] = rewards[0]["tier"]
            customer["tier_name"] = rewards[0]["rewardName"]
            customer["next_tier"] = rewards[1]["tier"]
            customer["next_tier_name"] = rewards[1]["rewardName"]
            customer["next_tier_progress"] = (points / rewards[1]["points"]) * 100
        elif len(rewards) == 1:
            customer["tier"] = rewards[0]["tier"]
            customer["tier_name"] = rewards[0]["rewardName"]
            customer["next_tier"] = ""
            customer["next_tier_name"] = ""
            customer["next_tier_progress"] = 0.00
        else:
            # see if customer is too high or too low to know where their tier is
            top_reward = list(db.rewards.find({}).sort("points", -1).limit(1))[0]
            lowest_reward = list(db.rewards.find({}).sort("points", 1).limit(2))

            if top_reward["points"] < points:
                customer["tier"] = top_reward["tier"]
                customer["tier_name"] = top_reward["rewardName"]
                customer["next_tier"] = ""
                customer["next_tier_name"] = ""
                customer["next_tier_progress"] = 0.00
            else:
                customer["tier"] = lowest_reward[0]["tier"]
                customer["tier_name"] = lowest_reward[0]["rewardName"]
                customer["next_tier"] = lowest_reward[1]["tier"]
                customer["next_tier_name"] = lowest_reward[1]["rewardName"]
                customer["next_tier_progress"] = 0.00


        try:
            db.customers.insert_one(customer)
        except Exception as err:
            print("ERROR: {}".format(err))
            json_response["success"] = False
        
        self.write(json.dumps(json_response))

