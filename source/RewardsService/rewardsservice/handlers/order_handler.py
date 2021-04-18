import json
import logging
import math

import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class OrderHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):

        logger = logging.getLogger()
        logger.info("/order endpoint hit")

        email_address = self.get_argument("emailAddress")
        order_total = float(self.get_argument("orderTotal"))

        points_earned = math.floor(order_total)
        logger.info("email: %s, order total: $%.2f, points earned: %i", email_address, order_total, points_earned)

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        # Existing customer
        try:
            old_points = db.customers.find_one({"emailAddress": email_address})["points"]
        except Exception as e:
            logger.exception(e)
            old_points = 0

        if old_points < 1000:
            points = points_earned + old_points

            if (math.floor(points / 100) * 100) >= 1000:
                points_query = 1000
                points = 1000
                next_tier = "max"
                next_reward_name = "max"
                next_tier_progress = "max"
            else:
                points_query = math.floor(points / 100) * 100
                next_tier_progress = (points - points_query) / 100

            tier_data = db.rewards.find({"points": points_query})

            for d in tier_data:
                tier = d['tier']
                reward_name = d['rewardName']

            next_tier_data = db.rewards.find({"points": points_query + 100})
            for d in next_tier_data:
                next_tier = d['tier']
                next_reward_name = d['rewardName']

            db.customers.find_one_and_update({"emailAddress": email_address},
                                             {
                                                 "$set": {
                                                     "tier": tier,
                                                     "rewardName": reward_name,
                                                     "points": points,
                                                     "nextTier": next_tier,
                                                     "nextRewardName": next_reward_name,
                                                     "nextTierProgress": next_tier_progress
                                                 }
                                             }, upsert=True)
