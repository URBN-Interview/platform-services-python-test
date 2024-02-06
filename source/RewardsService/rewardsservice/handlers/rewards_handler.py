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


class RewardsHandler(tornado.web.RequestHandler):

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

    @coroutine
    def get(self):
        rewards = list(self.db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))

    @coroutine
    def post(self):
        try:
            data = json.loads(self.request.body.decode("utf-8"))

            try:
                validate(data, schema=self.schema)
            except ValidationError as ve:
                self.set_status(400)
                self.write(json.dumps({"error_message": ve.message}))
                self.finish()

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
            rewards_data.sort(key=operator.itemgetter("points"), reverse=True)

            order_total = data.get('order_total', 0.0)
            try:
                matching_reward = next((
                    item for item in rewards_data if order_total >= item["points"]
                ))
            except StopIteration:
                matching_reward = None
            self.write(json.dumps(matching_reward))
            # self.write(json.dumps({"status": "Order Created"}))
            self.finish()
        except Exception as e:
            self.set_status(400)
            self.write(json.dumps({"error_message": f"{str(e)}"}))
