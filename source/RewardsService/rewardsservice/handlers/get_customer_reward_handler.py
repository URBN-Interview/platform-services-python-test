import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class GetCustomerRewardHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client.Rewards
        try:
            email = self.get_argument('email')
            customer_rewards = db.customer_rewards.find_one({"email": email},{"_id": 0})
            if not customer_rewards:
                # if no customer assiociated with email, set error response json
                customer_rewards = {
                                    "status": 404, "error": "Not Found", 
                                    "message": "Could not find record with customer matching email.", 
                                    "details": {"email": email}
                                    }
            self.write(json.dumps(customer_rewards))
            # will do some searching
        except Exception as e:
            self.write("an issue occured")
            logger.info("exception: {0}".format(e))