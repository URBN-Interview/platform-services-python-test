import datetime
import operator
import re
import json

import tornado.web
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pymongo import MongoClient
from tornado.gen import coroutine

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
dt_format = "%Y/%m/%d %H:%M:%S"


class OrdersHandler(tornado.web.RequestHandler):

    client = MongoClient("mongodb", 27017)
    db = client["Rewards"]
    schema = {
        "type": "object",
        "properties": {
            "email": {"type": "string"},
            "order_total": {"type": "number"},
        },
        "required": ["email", "order_total"],
    }

    @staticmethod
    def _serialize_data(data):
        for item in data:
            item["created"] = item["created"].strftime(dt_format)
            item["updated"] = item["updated"].strftime(dt_format)

    @coroutine
    def get(self):
        orders = list(self.db.orders.find({}, {"_id": 0}))
        self._serialize_data(orders)
        self.write(json.dumps(orders))

    @coroutine
    def post(self):
        try:
            data = json.loads(self.request.body.decode("utf-8"))

            # input body validation
            try:
                validate(data, schema=self.schema)
            except ValidationError as ve:
                self.set_status(400)
                self.write(json.dumps({"error_message": ve.message}))
                self.finish()

            # email validation
            # tried using external package was getting installation
            # error in docker so moved to regex
            if re.fullmatch(regex, data.get("email")):
                pass
            else:
                self.set_status(422)
                self.write(json.dumps({"error_message": "Invalid Email ID"}))
                self.finish()

            record = {
                "email": data.get("email"),
                "order_total": data.get("order_total", 0.0)
            }
            rewards_data = list(self.db.rewards.find({}, {"_id": 0}))
            # sort by points descending true
            rewards_data.sort(key=operator.itemgetter("points"), reverse=True)

            # fetch reward match
            order_total = data.get('order_total', 0.0)
            try:
                matching_reward = next((
                    item for item in rewards_data if order_total >= item["points"]
                ))
            except StopIteration:
                matching_reward = None

            # update record
            if matching_reward:
                record.update({
                    "reward_points": matching_reward["points"],
                    "reward_tier": matching_reward["tier"],
                    "reward_tier_name": matching_reward["rewardName"]
                })

                # finding the next tier
                if matching_reward != rewards_data[0]:
                    next_tier = rewards_data[rewards_data.index(matching_reward) - 1]
                    record.update({
                        "next_reward_tier": next_tier["tier"],
                        "next_reward_tier_name": next_tier["rewardName"],
                        "next_reward_tier_progress": (order_total / next_tier["points"]) * 100
                    })

            # metadata
            record["created"] = datetime.datetime.now()
            record["updated"] = datetime.datetime.now()

            self.db.orders.insert(record)

            self.set_status(201)
            self.write(json.dumps({"status": "Order Created"}))
            self.finish()
        except Exception as e:
            self.set_status(400)
            self.write(json.dumps({"error_message": f"{str(e)}"}))


class OrderHandler(tornado.web.RequestHandler):
    client = MongoClient("mongodb", 27017)
    db = client["Rewards"]

    def get(self):
        query = {}
        email = self.get_query_argument("email", default=None)
        if not email:
            self.write(json.dumps({"error_message": "Please provide email as query params"}))
            self.finish()
        query["email"] = email
        order = self.db.orders.find_one(query, {"_id": 0})
        order["created"] = order["created"].strftime(dt_format)
        order["updated"] = order["updated"].strftime(dt_format)
        self.write(json.dumps(order))
