import json
import math

import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        email_address = self.get_argument("emailAddress")
        order_total = int(self.get_argument("orderTotal"))
        points_earned = math.floor(order_total)

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        # Existing customer
        old_points = db.customers.find_one({"emailAddress": email_address})["points"]
        if old_points < 1000:
            new_points = points_earned + old_points

            if (math.floor(new_points / 100) * 100) > 1000:
                points_query = 1000
            else:
                points_query = math.floor(new_points / 100) * 100

            tier_data = db.rewards.find({"points": points_query})
            next_tier_data = db.rewards.find({"points": points_query + 100})

            db.customers.find_one_and_update({"emailAddress": email_address},
                                             {
                                                 "$set": {
                                                     "tier": tier_data["tier"],
                                                     "rewardName": tier_data["rewardName"],
                                                     "points": tier_data["points"],
                                                     "nextTier": next_tier_data["tier"],
                                                     "nextRewardName": next_tier_data["rewardName"],
                                                     "nextTierProgress": new_points - points_query / 100
                                                 }
                                             })

        # else if:
