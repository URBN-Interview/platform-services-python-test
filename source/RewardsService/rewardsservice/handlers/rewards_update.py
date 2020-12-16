# written by Edward Barbezat 12/16/20
import json
import math
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class RewardsUpdate(tornado.web.RequestHandler):
    # accept customer's order data then calculate and store rewards data into db
    @coroutine
    def get(self):
        email = self.get_argument('email')
        amountSpent = float(self.get_argument('amount'))
        client = MongoClient("mongodb", 27017)
        usersDB = client["Users"]

        points = math.floor(amountSpent) # 1 point for every dollar spent at purchase
        existingUser = usersDB.users.find_one({"email" : email})

        if (existingUser != None):
            prevPoints = existingUser["points"]
            points = points + prevPoints 

        # aggregating rewards information
        rewardsDB = client["Rewards"]
        rewardTierPoints = rewardsDB.rewards.distinct('points')
        rewardTiers = rewardsDB.rewards.distinct('tier')
        # different approach to tier names since alphanumeric sorting places items out of order (5% off placed after 10% off for example)
        unsortedTierNames = rewardsDB.rewards.find({}, {'rewardName':1, '_id':0})
        rewardTierNames = []
        for name in unsortedTierNames:
            rewardTierNames.append(name['rewardName'])

        # find users tier based on points obtained
        for index, pointVal in enumerate(rewardTierPoints):
            if points >= pointVal:
                tier = rewardTiers[index]
                tierName = rewardTierNames[index]
            elif points <= 100: # minimum amount before a tier is specified
                tier = "N/A"
                tierName = "N/A"
            else:
                break

        if (index < len(rewardTiers) - 1):
            nextTier = rewardTiers[index]
            nextTierName = rewardTierNames[index]
            try:
                nextTierProgress = (rewardTierPoints[index] - points) / points
            except:
                print("Something went wrong updated the next tier progress") # only error I can imagine is divide by zero, in case of a free item for example
                nextTierProgress = 0
        else:
            #TODO find out if more specific behavior required once max tier is reached
            nextTier = "N/A"
            nextTierName = "N/A"
            nextTierProgress = "N/A"

        # update DB
        userdata = {"email" : email, "points" : points, "tier" : tier, "tierName" : tierName, "nextTier" : nextTier, "nextName" : nextTierName, "nextProgress" : nextTierProgress}

        if (existingUser == None):
            try:
                usersDB.users.insert_one(userdata)
                print("Sucessfully added new user " + email + " to the database")
            except:
                print("Something went wrong trying to update the database")
        else:
            try:
                usersDB.users.replace_one({"email" : email}, userdata)
                print("Successfully updated existing user " + email + "'s information")
            except:
                print("Something went wrong trying to update the database")