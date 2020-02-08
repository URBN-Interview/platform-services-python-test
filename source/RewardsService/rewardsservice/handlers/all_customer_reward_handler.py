import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class AllCustomerRewardHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client.Rewards
        try:
            all_rewards = list(db.userRewards.find({}, {"_id": 0}))

            self.write(json.dumps(all_rewards))
            #self.write('hjkhhkhkhkh')
                # will do some searching
        except AssertionError:
            self.write("no params")