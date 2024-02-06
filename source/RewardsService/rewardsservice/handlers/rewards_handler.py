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
        db = self.client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
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
            self.write(json.dumps({"status": "success"}))
        except Exception as e:
            self.set_status(400)
            self.write(json.dumps({"error_message": f"{str(e)}"}))
