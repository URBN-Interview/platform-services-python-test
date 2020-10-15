import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class OrdersHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        print("Enabling CORS...")
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
            clients = list(col.find({}, {"_id": 0}))
            clients = sorted(clients, key=lambda x : x['email'], reverse=False)
            self.write(json.dumps(clients))
        else:
            self.write(json.dumps(self.getClientDataByEmail(email[0])))

    @coroutine
    def post(self):
        orderEmailAddress = self.get_body_argument("email")
        orderAmount = self.get_body_argument("amount")

        client_data = self.processClientData(orderEmailAddress, orderAmount)
        self.write(json.dumps(client_data, default=str))

    def processClientData(self, orderEmailAddress, orderAmount):
        rewards = self.getSortedRewardTierData()
        existingEntry = self.getClientDataByEmail(orderEmailAddress)

        orderAmount = orderAmount.split(".")[0]
        if(len(existingEntry) > 0):
            existingEntry = existingEntry[0]
            orderAmount = int(orderAmount) + int(existingEntry['points'])

        previous = ''
        previousTier = ''
        previousName = ''
        current = ''
        currentTier = ''
        currentName = ''
        nextTierProgress = ''
        for reward in rewards:
            current = int(reward['points'])
            if(current < int(orderAmount)):
                currentTier = reward['tier']
                currentName = reward['rewardName']
                break
            previous = current
            previousTier = reward['tier']
            previousName = reward['rewardName']
            nextTierProgress = reward['points'] - int(orderAmount)

        client_data = {"_id": orderEmailAddress, "email": orderEmailAddress, "points": orderAmount, "tier": currentTier, "tierName": currentName, "nextTier": previousTier, "nextTierName": previousName, "nextTierProgress": nextTierProgress}

        self.updateData(client_data)
        return client_data

    def getSortedRewardTierData(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        rewards = sorted(rewards, key=lambda x : x['points'], reverse=True)
        return rewards

    def updateData(self, client_data):
        client = MongoClient("mongodb", 27017)
        col = client["Rewards"]["client_reward"]
        col.replace_one({"email": client_data['email']}, client_data, True)

    def getClientDataByEmail(self, email):
        client = MongoClient("mongodb", 27017)
        col = client["Rewards"]["client_reward"]
        return list(col.find({"email": email}, {"_id": 0}))
