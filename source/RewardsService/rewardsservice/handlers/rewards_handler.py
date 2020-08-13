import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

from pymongo import MongoClient
import json

class RewardsHandler(tornado.web.RequestHandler):

    @coroutine #async function
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
        raise tornado.gen.Return(rewards) # return the list of reward tiers


class Init(tornado.web.RequestHandler):
    def get(self):
        self.write({'message':'hello world'})


class CustomerData(RewardsHandler):

    #determine tier (helper function)
    def tier(self, total):
        if total < 100:
            return "not yet"
        elif total < 200:
            return "A"
        elif total < 300:
            return "B"
        elif total < 400:
            return "C"
        elif total < 500:
            return "D"
        elif total < 600:
            return "E"
        elif total < 700:
            return "F"
        elif total < 800:
            return "G"
        elif total < 900:
            return "H"
        elif total < 1000:
            return "I"
        else:
            return "J"

    #use literal rewards array temporarily (ideal would be to pull from RewardsHandler Class)
    tiers = [
        { "tier": "A", "rewardName": "5% off purchase", "points": 100 },
        { "tier": "B", "rewardName": "10% off purchase", "points": 200 },
        { "tier": "C", "rewardName": "15% off purchase", "points": 300 },
        { "tier": "D", "rewardName": "20% off purchase", "points": 400 },
        { "tier": "E", "rewardName": "25% off purchase", "points": 500 },
        { "tier": "F", "rewardName": "30% off purchase", "points": 600 },
        { "tier": "G", "rewardName": "35% off purchase", "points": 700 },
        { "tier": "H", "rewardName": "40% off purchase", "points": 800 },
        { "tier": "I", "rewardName": "45% off purchase", "points": 900 },
        { "tier": "J", "rewardName": "50% off purchase", "points": 1000 }
    ]

    def nextTier(self, tier):
        if tier == "F":
            return "You are top tier!"
        for i in range(len(self.tiers)):
            if self.tiers[i]["tier"] == tier:
                return self.tiers[i + 1]["tier"]

    def TierName(self, tier):
        if tier == "F":
            return "No more upgrades!"
        for i in range(len(self.tiers)):
            if self.tiers[i]["tier"] == tier:
                return self.tiers[i]["rewardName"]

    def nextTierPoints(self, tier):
        if tier == "F":
            return "You are top tier!"
        for i in range(len(self.tiers)):
            if self.tiers[i]["tier"] == tier:
                return self.tiers[i + 1]["points"]

    @coroutine #async function
    def post(self):

        #calculate inputs to store into customer information database
        customerInfo = json.loads(self.request.body.decode('utf-8')) # {'email': 'xx', 'order-total': 'xxx'}
        email = customerInfo['e-mail']
        orderTotal = customerInfo['order-total'] # 100.80
        points = int(float(orderTotal)) # 100
        rewardsTier = self.tier(float(orderTotal)) # "A"
        rewardsTierName = self.TierName(rewardsTier) #"5% off purchase"
        nextRewardTier = self.nextTier(rewardsTier) # "B"
        nextRewardTierName = self.TierName(nextRewardTier) #"10% off purchase"
        progress = round(float(orderTotal) / self.nextTierPoints(rewardsTier), 2)


        client = MongoClient("mongodb", 27017)
        # create cusomer database
        db = client["Customer"]

        #schema for customer db
        input = {
            "Email Address": email,
            "Reward Points": points,
            "Reward Tier": rewardsTier,
            "Reward Tier Name":  rewardsTierName,
            "Next Reward Tier": nextRewardTier,
            "Next Reward Tier Name": nextRewardTierName,
            "Next Reward Tier Progress": progress
        }

        #inserts the customer in the 'customer' collection
        db.customers.insert(input)

        #output data inserted into db on post req
        self.write({
            "Email Address": email,
            "Reward Points": points,
            "Reward Tier": rewardsTier,
            "Reward Tier Name":  rewardsTierName,
            "Next Reward Tier": nextRewardTier,
            "Next Reward Tier Name": nextRewardTierName,
            "Next Reward Tier Progress": progress
        })

        # return input


class CustomerSummary(CustomerData):

    @coroutine
    def post(self):
        customerInfo = json.loads(self.request.body.decode('utf-8')) # {'email': 'xx'}
        email = customerInfo['e-mail']

        # get rewards data for customer
        client = MongoClient("mongodb", 27017)
        db = client["Customer"]
        output = db.customers.find_one({"Email Address": email})

        #get rid of non-JSON serializable key (ObjectId)
        customerData = {k: v for k, v in output.items() if k != "_id"}

        self.write({"output": customerData})


class AllCustomers(CustomerData):

    @coroutine
    def get(self):
        # get rewards data for all customers
        client = MongoClient("mongodb", 27017)
        db = client["Customer"]
        output = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(output))

