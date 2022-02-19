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

        # email check
        # only one email per customer to keep get data in customer handler clean
        email_check = list(db.customers.find(
            {"email": json_request["email"]}
        ))

        if len(email_check) == 0:
            # build customer data struct/collection entry
            points = int(json_request["total"])
            customer = {
                "email": json_request["email"],
                "points": points,
                "tier": None,
                "tier_name": None,
                "next_tier": None,
                "next_tier_name": None,
                "next_tier_progress": 0
            }

            # get tier information from current points to next tier
            # order by points
            reward_query = db.rewards.find({
                "points": {"$gte": points}
            }).sort("points", 1).limit(2)
            rewards = list(reward_query)

            # add reward data to customer
            customer["tier"] = rewards[0]["tier"]
            customer["tier_name"] = rewards[0]["rewardName"]
            customer["next_tier"] = rewards[1]["tier"]
            customer["next_tier_name"] = rewards[1]["rewardName"]
            customer["next_tier_progress"] = (points / rewards[1]["points"]) * 100

            try:
                db.customers.insert_one(customer)
            except Exception as err:
                print("ERROR: {}".format(err))
                json_response["success"] = False
        else:
            json_response["success"] = False
        
        self.write(json.dumps(json_response))

