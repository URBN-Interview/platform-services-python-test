import json
import math
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class OrderCalculator():
    
    def get_reward_points(self, order_amount):
        return math.floor(float(order_amount))

    def get_tier_record(self, reward_points):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        reward_points_nearest_hundred = math.floor(reward_points/100) * 100
        return db.rewards.find_one({"points": reward_points_nearest_hundred})
    
    def get_next_tier_record(self, tier):
        next_tier_record = None
        if tier == 'A':
            next_tier_record = OrderCalculator.get_tier_record(self, 200)
        elif tier == 'B':
            next_tier_record = OrderCalculator.get_tier_record(self, 300)
        elif tier == 'C':
            next_tier_record = OrderCalculator.get_tier_record(self, 400)
        elif tier == 'D':
            next_tier_record = OrderCalculator.get_tier_record(self, 500)
        elif tier == 'E':
            next_tier_record = OrderCalculator.get_tier_record(self, 600)
        elif tier == 'F':
            next_tier_record = OrderCalculator.get_tier_record(self, 700)
        elif tier == 'G':
            next_tier_record = OrderCalculator.get_tier_record(self, 800)
        elif tier == 'H':
            next_tier_record = OrderCalculator.get_tier_record(self, 900)
        elif tier == 'I':
            next_tier_record = OrderCalculator.get_tier_record(self, 1000)
        return next_tier_record

    def get_percentage_to_next_tier(self, reward_points, next_tier_points):
        return (next_tier_points - reward_points) / 100

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
        db = client["Orders"]
        reward_points = OrderCalculator.get_reward_points(self, self.get_body_argument("order total"))
        tier_record = OrderCalculator.get_tier_record(self, reward_points)
        next_tier_record = OrderCalculator.get_next_tier_record(self, tier_record["tier"])
        percentage_to_next_tier = OrderCalculator.get_percentage_to_next_tier(self, reward_points, next_tier_record["points"])
        db.orders.remove()
        db.orders.insert({
            "emailAddress": self.get_body_argument("email address"),
            "rewardPoints": tier_record["points"],
            "rewardTier": tier_record["tier"],
            "rewardTierName": tier_record["rewardName"],
            "nextRewardTier": next_tier_record["tier"],
            "nextRewardTierName": next_tier_record["rewardName"],
            "nextRewardTierProgress": percentage_to_next_tier,
            })
        orders = list(db.orders.find({}, {"_id": 0}))
        self.write(json.dumps(orders))


