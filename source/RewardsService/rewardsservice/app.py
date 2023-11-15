#!/usr/bin/env python
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import options

from pymongo import MongoClient

from settings import settings
from url_patterns import url_patterns

rewards_info=[
    { "tier": "A", "rewardName": "5% off purchase", "points": 100 },
    { "tier": "B", "rewardName": "10% off purchase", "points": 200 },
    { "tier": "C", "rewardName": "15% off purchase", "points": 300 },
    { "tier": "D", "rewardName": "20% off purchase", "points": 400 },
    { "tier": "E", "rewardName": "25% off purchase", "points": 500 },
    { "tier": "F", "rewardName": "30% off purchase", "points": 600 },
    { "tier": "G", "rewardName": "35% off purchase", "points": 700 },
    { "tier": "H", "rewardName": "40% off purchase", "points": 800 },
    { "tier": "I", "rewardName": "45% off purchase", "points": 900 },
    { "tier": "J", "rewardName": "50% off purchase", "points": 1000 }
]

class App(tornado.web.Application):
    def __init__(self, urls):
        self.logger = logging.getLogger(self.__class__.__name__)

        tornado.web.Application.__init__(self, urls, **settings)

app = App(url_patterns)

class CalculateRewards(tornado.web.RequestHandler):
    def post(self):
        try:
            email=self.get_argument("email")
            order_total="{:.2f}".format(float(self.get_argument("order_total")))
            
            # Does this work instead of floor function from math
            reward_pts=int(float(order_total))

            # Combine functions?
            reward_name=self.calculate_reward_name(reward_pts)
            
            tier=self.calculate_rewards(reward_pts)

            # Store in DB
            self.store_rewards_info(email, reward_pts, reward_name, tier)

            # Response
            response={
                "email":email,
                "reward_pts":reward_pts,
                "reward_name":reward_name,
                "tier":tier
            }
            self.write({"status":"success"})
        except Exception as e:
            self.set_status(400)
            self.write({"status":"error","message":str(e)})

    # Logic here or in load_mongo_data file?
    def calculate_rewards(email, order_ttl):
        #from load_mongo_data import calculate_rewards
        points_accrued=int(float(order_ttl))
        cust_reward=None

        for reward in rewards_info:
            if points_accrued >= reward['points']:
                cust_reward={
                    "email":email,
                    "reward_pts":points_accrued,
                    "reward_name":reward['reward_name'],
                    "reward_tier":reward['tier']
                }
            else:
                break
        return cust_reward
    

    def store_rewards_info(self, email, reward_pts, reward_name, tier):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        collection=db["customer_rewards"]

        data={
            "email":email,
            "reward_pts":reward_pts,
            "reward_name":reward_name,
            "tier":tier
        }
        collection.insert(data)
    

def main():
    logger = logging.getLogger()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)

    logger.info('Tornado server started on port {}'.format(options.port))

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logger.info("\nStopping server on port {}".format(options.port))


if __name__ == "__main__":
    main()
