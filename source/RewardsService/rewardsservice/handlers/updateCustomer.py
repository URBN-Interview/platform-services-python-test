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
            currentPoints = user["rewardPoints"]
            totalPoints = math.floor(orderTotal) + currentPoints
            db.Customer.update({"$set": {"rewardPoints": totalPoints}})
        else:
            totalPoints = math.floor(orderTotal)
            db.Customer.insert({email: email, points: math.floor(orderTotal)})

        updatedUser = {
            "email": email,
            "rewardPoints": totalPoints,
            "tier": "",
            "tierName": "",
            "nextTier": "",
            "nextTierName": "",
            "progress": ""
        }

        if(totalPoints > 1000):
            updatedUser["tier"] = "J"
            updatedUser["tierName"] = "50% off purchase"
            updatedUser["nextIter"] = "N/A"
            updatedUser["nextTierName"] = "N/A"
            updatedUser["progress"] = "N/A"

        elif(totalPoints < 100):
            updatedUser["tier"] = "N/A"
            updatedUser["tierName"] = "N/A"
            updatedUser["nextIter"] = "A"
            updatedUser["nextTierName"] = "5% off purchase"
            updatedUser["progress"] = str((totalPoints % 100)/100)+"%"

        else:
            dbupdatedUser = client["updatedUser"]
            # Finding flooredPoints to find equivalent points in 100s to find appropriate category
            flooredPoints = (totalPoints//100)*100
            currentData = dbupdatedUser.updatedUser.find(
                {points: flooredPoints})
            updatedUser["tier"] = currentData["tier"]
            updatedUser["tierName"] = currentData["tierName"]
            updatedUser["nextTier"] = currentData["nextTier"]
            updatedUser["nextTierName"] = currentData["nextTierName"]
            updatedUser["progress"] = (100-totalPoints/100)

        db.Customer.update({'email': email}, updatedUser, {upsert: True})
        print("Updated")
        # self.write("Updated")
