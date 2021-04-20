import json
import tornado.web
import math

from pymongo import MongoClient
from tornado.gen import coroutine


class updateCustomer(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Customer"]
        orderTotal = self.get_arguments("orderTotal")
        email = self.get_arguments("email")
        user = db.find({"email": email})
        totalPoints = 0
        if(user):
            currentPoints = user["points"]
            totalPoints = math.floor(orderTotal) + currentPoints
            db.Customer.update({"$set": {"points": totalPoints}})
        else:
            totalPoints = math.floor(orderTotal)
            db.Customer.insert({email: email, points: math.floor(orderTotal)})

        rewards = {
            "tier": "",
            "tierName": "",
            "nextTier": "",
            "nextTierName": "",
            "progress": ""
        }

        if(totalPoints > 1000):
            rewards["tier"] = "J"
            rewards["tierName"] = "50% off purchase"
            rewards["nextIter"] = "N/A"
            rewards["nextTierName"] = "N/A"
            rewards["progress"] = "N/A"

        elif(totalPoints < 100):
            rewards["tier"] = "N/A"
            rewards["tierName"] = "N/A"
            rewards["nextIter"] = "A"
            rewards["nextTierName"] = "5% off purchase"
            rewards["progress"] = str((100-totalPoints/100))*100 + "%")

        else:
            dbRewards=client["Rewards"]
            # Finding flooredPoints to find equivalent points in 100s to find appropriate category
            flooredPoints=(totalPoints//100)*100
            currentData=dbRewards.rewards.find({points: flooredPoints})
            rewards["tier"]=currentData["tier"]
            rewards["tierName"]=currentData["tierName"]
            rewards["nextTier"]=currentData["nextTier"]
            rewards["nextTierName"]=currentData["nextTierName"]
            rewards["progress"]=str((100-totalPoints/100))*100 + "%")
