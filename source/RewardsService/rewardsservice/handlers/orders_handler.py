import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class OrdersHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @coroutine
    def options(self):
        self.set_status(200)
        self.finish()

    @coroutine
    def get(self):
        email = self.get_arguments("email")
        if(email == []):
            client = MongoClient("mongodb", 27017)
            col = client["Rewards"]["client_reward"]
            rewards = list(col.find({}, {"_id": 0}))
            self.write(json.dumps(rewards))
        else:
            client = MongoClient("mongodb", 27017)
            col = client["Rewards"]["client_reward"]
            reward = list(col.find({"email": email[0]}, {"_id": 0}))
            self.write(json.dumps(reward))

    @coroutine
    def post(self):
        orderEmailAddress = self.get_body_argument("email")
        orderAmount = self.get_body_argument("amount")

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        #sorted_obj = dict(rewards)
        rewards = sorted(rewards, key=lambda x : x['points'], reverse=True)

        previous = ''
        previousTier = ''
        previousName = ''
        current = ''
        currentTier = ''
        currentName = ''
        for reward in rewards:
            current = int(reward['points'])
            if(current < int(orderAmount)):
                currentTier = reward['tier']
                currentName = reward['rewardName']
                #print(str(current) + ' - ' + reward['tier'] + ' - ' + reward['rewardName'])
                break
            previous = current
            previousTier = reward['tier']
            previousName = reward['rewardName']

        col = db["client_reward"]
        col.insert_one({"email":orderEmailAddress, "points": orderAmount, "tier": previousTier, "tierName": previousName, "nextTier": currentTier, "nextTierName": currentName, "nextTierProgress": 0})

        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + orderEmailAddress + " - " + orderAmount)
