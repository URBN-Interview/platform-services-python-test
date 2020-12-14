import json
import re

import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

from rewardsservice.utils import email_is_valid


class CustomerRewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        email = self.get_argument('email')

        if email_is_valid(email):
            customer_rewards = list(db.customerdata.find({"email": email}, {"_id": 0}))
            if len(customer_rewards) < 1:
                self.send_error(404)
            else:
                self.write(json.dumps(customer_rewards))
        else:
            self.clear()
            self.set_status(400)
            self.finish("<html><body>Invalid email</body></html>")
