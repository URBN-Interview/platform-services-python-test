import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        json_response = {}

        try:
            client = MongoClient("mongodb", 27017)
        
            # rewards
            db = client["Rewards"]
            rewards = list(db.rewards.find({}, {"_id": 0}))
            
            json_response = {"rewards": rewards}
        except Exception as err:
            raise err

        self.write(json.dumps(json_response))

    # handle customer information and commit to database
    @coroutine
    def post(self):
        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            json_response = {"success": False}

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
                # customer points nothing is greater than, set at highest
                top_reward = list(db.rewards.find({}).sort("points", -1).limit(1))[0]
                customer["tier"] = top_reward["tier"]
                customer["tier_name"] = top_reward["rewardName"]
                customer["next_tier"] = ""
                customer["next_tier_name"] = ""
                customer["next_tier_progress"] = 0.00

            # insert new customer to collection
            db.customers.insert_one(customer)
            json_response["success"] = True
        except Exception as err:
            raise err
        
        self.write(json.dumps(json_response))

