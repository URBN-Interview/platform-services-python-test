import json
from bson import ObjectId

from tornado.web import RequestHandler
from tornado import gen
from pymongo import ASCENDING, DESCENDING

from db_connection import DBConnection

class CustomerRewardsHandler(RequestHandler):

    def initialize(self):
        self.db = DBConnection.get_client()['Rewards']
        self.top_reward_prg = self.get_top_reward()

    def _calculate_points(self, amount, available_points=0):
        return available_points + int(amount or 0)

    def _calculate_progress(self, points):
        if points > self.top_reward_prg.get("points"):
            return 100
        curr_reward_prg = self.get_current_reward_program(points)
        nxt_reward_prg = self.get_next_reward_program(points)
        diff = nxt_reward_prg.get("points") - curr_reward_prg.get("points", 0)
        rem = points % 100 if points > 100 else points
        return round((rem/diff) * 100, 2)

    def get_customer_available_points(self, email):
        customer = self.db.customers.aggregate([
            {
                "$match": {"emailId": email}
            },
            {
                "$group": {
                    "_id": "$emailId",
                    "totalPoints": {"$sum": "$earnedPoints"},
                },
            }
        ])
        customer = list(customer)
        return customer[0].get("totalPoints") if customer else 0

    def get_top_reward(self):
        return self.db.rewards.find_one({}, sort=[("points", DESCENDING)]) or {}

    def get_current_reward_program(self, points):
        lower_bound = points - 100
        return self.db.rewards.find_one({
            "$and": [{"points": {"$gt": lower_bound}}, {"points": {"$lte": points}}]
        }) or {}

    def get_next_reward_program(self, points):
        upper_bound = points + 100
        return self.db.rewards.find_one({
            "$and": [{"points": {"$gt": points}}, {"points": {"$lte": upper_bound}}]
        }) or {}

    async def post(self):
        try:
            customer = json.loads(self.request.body)
            email = customer.get("emailId")
            available_points = self.get_customer_available_points(email)
            if available_points < self.top_reward_prg.get("points"):
                points = self._calculate_points(customer.get("orderTotal"), available_points)
                curr_reward_prg = self.get_current_reward_program(points)
                nxt_reward_prg = self.get_next_reward_program(points)
                customer.update({
                    "_id": str(ObjectId()),
                    "earnedPoints": int(customer.get("orderTotal") or 0),
                    "points": points,
                    "tier": curr_reward_prg.get("tier"),
                    "rewardName": curr_reward_prg.get("rewardName"),
                    "nextTier": nxt_reward_prg.get("tier"),
                    "nextRewardName": nxt_reward_prg.get("rewardName"),
                    "nextRewardTierAwayPercentage": (100 - self._calculate_progress(points)),
                })
                del customer["orderTotal"]
                await self.db.customers.insert_one(customer)
                self.set_status(201)
                self.write({"message": "Customer rewards created successfully!"})
            else:
                self.set_status(200)
                self.write({"message": "You cannot earn more rewards as you have reached the top."})
        except Exception as e:
            err_msg = "Error while creating customer rewards: {}".format(e)
            self.set_status(500)
            self.write({"message": err_msg})

    async def get(self):
        try:
            email = self.get_argument("email", None, True)
            condition = {"emailId": email} if email else {}
            customers_cursor = self.db.customers.find().sort([("emailId", ASCENDING), ("points", ASCENDING)])
            customers = await gen.maybe_future(list(customers_cursor))
            self.set_status(200)
            self.write(json.dumps(customers))
        except Exception as e:
            err_msg = "Error while getting customer rewards: {}".format(e)
            self.set_status(500)
            self.write({"message": err_msg})


class RewardsHandler(RequestHandler):

    async def get(self):
        try:
            db = DBConnection.get_client()["Rewards"]
            rewards = await gen.maybe_future(list(db.rewards.find({}, {"_id": 0})))
            self.set_status(200)
            self.write(json.dumps(rewards))
        except Exception as e:
            error_msg = "Error:{}".format(e)
            self.set_status(500)
            self.write(error_msg)
