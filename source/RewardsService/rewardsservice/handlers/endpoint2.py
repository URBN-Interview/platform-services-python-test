import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class Endpoint2(tornado.web.RequestHandler):
    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)

        # grab all rewards
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        
        # grab all users
        users = list(db.users.find({}, {"_id": 0}))

        # get email
        email = self.get_body_argument('email')

        db.users.find({"email": email})

        # grab user that is being searched
        # user_emails = [user['email'] for user in users]
        # if email in user_emails:
        #     for user in users:
        #         for key in user:
        #             if user['email'] == email:
                        # return self.write(json.dumps(user))
                        # break
