import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
import math

class OrdersHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        rewardsdb = client["Rewards"]
        customersdb = client["Customers"]


        email = self.get_argument("email","")
        orders = self.get_argument("orders","")



        existingCustomer = customersdb.customers.find_one({"email":email}, {"_id": 0})
        totalPoints = int(float(orders))
        
        rewards = list(rewardsdb.rewards.find({}, {"_id": 0}))

        reward = None
        nextReward = None
        if(totalPoints>0):
            if(existingCustomer):
                totalPoints += existingCustomer["points"]

                if(totalPoints<1000):
                    #Gets our reward tier that we are at and breaks after not getting next tier
                    for i in rewards:
                        if(totalPoints>=i["points"]):
                            reward = i
                        else:
                            nextReward = i
                            break
                    nextProgress = (totalPoints%100)/100
                    if(totalPoints<100):
                        reward = {"tier":"N/A","rewardName":"N/A"}

                    customersdb.customers.update({"email":email},{
                        "email":email,
                        "points":totalPoints,
                        "rewardsTier":reward["tier"],
                        "rewardName":reward["rewardName"],
                        "nextTier":nextReward["tier"],
                        "nextRewardName":nextReward["rewardName"],
                        "nextTierProgress":nextProgress
                    })
                else:
                    reward = {"tier":"J","rewardName":"50% off purchase","points":1000}
                    nextReward = {"nextTier":"N/A","nextRewardName":"N/A","nextTierProgress":"N/A"}
                    customersdb.customers.update({"email":email},{
                        "email":email,
                        "points":totalPoints,
                        "rewardsTier":reward["tier"],
                        "rewardName":reward["rewardName"],
                        "nextTier":nextReward["nextTier"],
                        "nextRewardName":nextReward["nextRewardName"],
                        "nextTierProgress":nextReward["nextTierProgress"]
                    })
            else:
                if(totalPoints<=1000):
                    #Gets our reward tier that we are at and breaks after not getting next tier
                    for i in rewards:
                        if(totalPoints>=i["points"]):
                            reward = i
                        else:
                            nextReward = i
                            break
                    nextProgress = totalPoints/nextReward["points"]
                    if(totalPoints<100):
                        reward = {"tier":"N/A","rewardName":"N/A"}

                    customersdb.customers.insert({
                        "email":email,
                        "points":totalPoints,
                        "rewardsTier":reward["tier"],
                        "rewardName":reward["rewardName"],
                        "nextTier":nextReward["tier"],
                        "nextRewardName":nextReward["rewardName"],
                        "nextTierProgress":nextProgress
                    })
                else:
                    reward = {"tier":"J","rewardName":"50% off purchase","points":1000}
                    nextReward = {"nextTier":"N/A","nextRewardName":"N/A","nextTierProgress":"N/A"}
                    customersdb.customers.insert({
                        "email":email,
                        "points":totalPoints,
                        "rewardsTier":reward["tier"],
                        "rewardName":reward["rewardName"],
                        "nextTier":nextReward["tier"],
                        "nextRewardName":nextReward["rewardName"],
                        "nextTierProgress":nextReward["nextTierProgress"]
                    })
        else:
            #Insert error message if there is time
            print("Invalid Number!")
        orderData = list(customersdb.customers.find({"email": email}, {"_id": 0}))
        self.write(json.dumps(orderData))
