import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerRewardsHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        email = self.get_argument("email", None, True)

        if email:
            result = db.customer_rewards.find_one({"email": email}, {"_id": 0})
        else:
            result = list(db.customer_rewards.find({}, {"_id": 0}))

        if not result:
            self.set_status(404)
            return

        self.write(json.dumps(result))
