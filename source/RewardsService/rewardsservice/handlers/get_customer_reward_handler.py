import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
import logging
logger = logging.getLogger(__name__)

class GetCustomerRewardHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client.Rewards
        try:
            email = self.get_argument('email')
            customer_reward = list(db.customer_rewards.find({"email": email},{"_id": 0}))
            self.write(json.dumps(customer_reward))
            # will do some searching
        except Exception as e:
            self.write("an issue occured")
            logger.info("exception: {0}".format(e))