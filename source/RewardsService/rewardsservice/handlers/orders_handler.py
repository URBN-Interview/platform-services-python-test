import json
import math
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

from rewardsservice.order_calculator import OrderCalculator

class OrdersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        self.write('<html><body><form action="/order" method="POST">'
                   '<label for="email">Email Address:</label>'
                   '<br>'
                   '<input type="text" name="email address">'
                   '<br>'
                   '<label for="order">Order Total:</label>'
                   '<br>'
                   '<input type="number" step="any" name="order total">'
                   '<br>'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer_record = OrderCalculator.get_email_record(self, self.get_body_argument("email address"), db)
        if customer_record is not None:
            OrdersHandler.add_order_to_existing_customer(self, db, customer_record)
        else:
            OrdersHandler.create_new_customer_record(self, db)
        customer = db.orders.find_one({"emailAddress": self.get_body_argument("email address")})
        self.write(json.dumps(customer, default=str))

    def create_new_customer_record(self, db):
        reward_points = OrderCalculator.get_reward_points(self, self.get_body_argument("order total"))
        tier_record = OrderCalculator.get_tier_record(self, reward_points)
        next_tier_record = OrderCalculator.get_next_tier_record(self, tier_record["tier"])
        percentage_to_next_tier = OrderCalculator.get_percentage_to_next_tier(self, reward_points, next_tier_record["points"])
        db.orders.insert({
            "emailAddress": self.get_body_argument("email address"),
            "rewardPoints": reward_points,
            "rewardTier": tier_record["tier"],
            "rewardTierName": tier_record["rewardName"],
            "nextRewardTier": next_tier_record["tier"],
            "nextRewardTierName": next_tier_record["rewardName"],
            "nextRewardTierProgress": percentage_to_next_tier,
            })

    def add_order_to_existing_customer(self, db, customer_record):
        reward_points = customer_record["rewardPoints"] + OrderCalculator.get_reward_points(self, self.get_body_argument("order total"))
        tier_record = OrderCalculator.get_tier_record(self, reward_points)
        next_tier_record = OrderCalculator.get_next_tier_record(self, tier_record["tier"])
        percentage_to_next_tier = OrderCalculator.get_percentage_to_next_tier(self, reward_points, next_tier_record["points"])
        db.orders.update(
            {"emailAddress":customer_record["emailAddress"]},
            {
                "$set":{
                    "rewardPoints":reward_points,
                    "rewardTier": tier_record["tier"],
                    "rewardTierName": tier_record["rewardName"],
                    "nextRewardTier": next_tier_record["tier"],
                    "nextRewardTierName": next_tier_record["rewardName"],
                    "nextRewardTierProgress": percentage_to_next_tier,
                    }
                }
            )
