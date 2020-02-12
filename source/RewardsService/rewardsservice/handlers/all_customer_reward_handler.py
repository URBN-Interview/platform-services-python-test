import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

import logging
logger = logging.getLogger(__name__)

class AllCustomerRewardHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client.Rewards
        try:
            all_rewards = list(db.customer_rewards.find({}, {"_id": 0}))

            self.write(json.dumps(all_rewards))
                # will do some searching
        except Exception as e:
            self.write("an issue occured")
            logger.info("exception: {0}".format(e))