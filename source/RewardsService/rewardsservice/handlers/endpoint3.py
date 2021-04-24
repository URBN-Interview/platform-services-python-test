import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class Endpoint3(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        # if 'users' in db.list_collection_names():
        #     pass
        # else:
        #     db.create_collection('users')
        
        # db.users.drop()
        # mycol = db["Users"]
        users = list(db.users.find({}, {"_id": 0}))

        db.users.insert({
            "email": "test@email.com", 
            "rewardPoints": 160, 
            "rewardTier": "A",
            "rewardTierName": "5% off purchase",
            "nextRewardTier": "B",
            "nextRewardTierName": "10% off purchase",
            "nextRewardTierProgress": "80%"
            })

        self.write(json.dumps(users))