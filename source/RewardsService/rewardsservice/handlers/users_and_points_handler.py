#!/usr/bin/env python
#endpoint 1
from pymongo import MongoClient
import tornado.web

import math
from tornado.gen import coroutine

class UsersAndPointsHandler(tornado.web.RequestHandler):
    #add new customer or update customer rewards data

    #find current tier that customer is on
    def findTier(self, db, points):
        if(points >= 1000):
            points = 1000

        point = int(points/100) * 100
        return db.rewards.find_one({"points": point})

    #find next tier customer is on
    def findNextTier(self, db, points):
        #if points >= 1000 just return 1000 tier
        if(points >= 1000):
            return db.rewards.find_one({"points": 1000})

        point = (int(points/100) + 1) * 100
        return db.rewards.find_one({"points": point})

    #get the percentage of the progress to next tier | return string
    def findProgress(self, curr, next):
        return str((next - curr) / 100) + "%"

    #create a query to update or create new customer/order
    def createQuery(self, db, points, email):
        reward = self.findTier(db,points);
        tier = ''
        tierName = ''

        if reward is not None:
            tier = reward["tier"]
            tierName = reward["rewardName"]

        nextReward = self.findNextTier(db, points);
        nextTier = nextReward["tier"]
        nextTierName = nextReward["rewardName"]

        if not tier:
            nextTierProgress = self.findProgress(0, nextReward["points"])
        else:
            nextTierProgress = self.findProgress(reward["points"], nextReward["points"])

        query = {"email": email, "points": points, "tier": tier, "tierName": tierName, "nextTier": nextTier, "nextTierName": nextTierName, "nextTierProgress": nextTierProgress}
        return query

    #post function | add customer if exsist or update rewards
    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        # get email | order total | points
        email = self.get_argument("email")
        total = float(self.get_argument("total"))

        #turn total into points
        points = int(math.floor(total))

        #check if email exsists or not in customer collection
        findEmailQuery = {"email": email}
        myCustomer = db.customers.find_one(findEmailQuery)

        if myCustomer is None:
            #create new customer
            newCustomer = self.createQuery(db, points, email)
            db.customers.insert_one(newCustomer)
        else:
            #get the points & add to points
            #check tier again! & do calculations | update customer
            updateCustomer = self.createQuery(db, points, email)
            db.customers.update_one(findEmailQuery, updateCustomer)
