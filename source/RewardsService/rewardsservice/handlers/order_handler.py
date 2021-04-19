import logging
import math

import tornado.web
from pymongo import MongoClient
from tornado.escape import json_decode
from tornado.gen import coroutine
from tornado.web import MissingArgumentError


class OrderHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        # set up logging
        logger = logging.getLogger()
        logger.info("/order endpoint hit")

        # try to retrieve email query param, throw MissingArgumentError if unable to
        try:
            request = json_decode(self.request.body)
            email_address = request['emailAddress']
            order_total = request['orderTotal']

            # calculate points earned from order total
            points_earned = math.floor(order_total)
            logger.info("email: %s, order total: $%.2f, points earned: %i", email_address, order_total, points_earned)

            # try to connect to DB, throw exception if unable to
            try:
                client = MongoClient("mongodb", 27017)
                db = client["Rewards"]
                logger.info("connected to DB.")
                try:
                    old_points = db.customers.find_one({"emailAddress": email_address})["points"]
                    logger.info("found customer")
                except Exception as e:
                    old_points = 0
                    logger.info("customer with email %s not yet in DB, creating...", email_address)

                # check if customer has reached max points, if so - don't add any more points
                if old_points < 1000:

                    # calculate new points for customer
                    points = points_earned + old_points

                    # update record to maximum status if updated points exceeds or equals max points
                    if (math.floor(points / 100) * 100) >= 1000:
                        points_query = 1000
                        points = 1000
                        next_tier = "max"
                        next_reward_name = "max"
                        next_tier_progress = "max"
                    # else, get the base value for the customer's rewards group & calculate tier progress
                    else:
                        points_query = math.floor(points / 100) * 100
                        next_tier_progress = (points - points_query) / 100

                    # pull rewards collection to find point tier data
                    tier_data = db.rewards.find({"points": points_query})
                    for d in tier_data:
                        tier = d['tier']
                        reward_name = d['rewardName']

                    next_tier_data = db.rewards.find({"points": points_query + 100})
                    for d in next_tier_data:
                        next_tier = d['tier']
                        next_reward_name = d['rewardName']

                    # update customer collection
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

            except Exception as e:
                logger.error("Can't connect to server. Exception: %s", e)

        except MissingArgumentError as mae:
            logger.error("Query parameter missing. Exception: %s", mae)
