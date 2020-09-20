#!/usr/bin/env python
#endpoint 1
from pymongo import MongoClient
import tornado.web

import math
from tornado.gen import coroutine

class UsersAndPointsHandler(tornado.web.RequestHandler):
    def findTier(self, db, points):
        """
        TODO: Find the current tier of the customer using their points.

        Parameters
        ----------
        db : MongoClient
            Database
        points : int
            Number of points customer has.

        Returns
        -------
        mongo document
            Return the first result you get with the query {"points": point}.
        """

        if(points >= 1000):
            points = 1000

        point = int(points/100) * 100
        return db.rewards.find_one({"points": point})

    def findNextTier(self, db, points):
        """
        TODO: Find the next tier of the customer using their points.

        Parameters
        ----------
        db : MongoClient
            Database
        points : int
            Number of points customer has.

        Returns
        -------
        mongo document
            If points >= 1000 (There are no more tiers after 1000.)
                Return the first result you get with the query {"points": 1000}.

            Return the first result you get with the query {"points": point}.
        """

        if(points >= 1000):
            return db.rewards.find_one({"points": 1000})

        point = (int(points/100) + 1) * 100
        return db.rewards.find_one({"points": point})

    def findProgress(self, curr, next):
        """
        TODO: Find percentage of progress made to get to next tier.

        Parameters
        ----------
        curr : int
            Current points a customer has.
        next : int
            The tier to reach.

        Returns
        -------
        string
            Return next-curr + "%"
        """

        if next - curr == 100:
            return "0%"

        return str(next - curr) + "%"

    def createQuery(self, db, points, email):
        """
        TODO: Create query to insert or update customer.

        Parameters
        ----------
        db : MongoClient
            Database
        points : int
            Number of points customer has.
        email : string
            Customer's email.

        Returns
        -------
        mongo query
            Return query
        """

        reward = self.findTier(db,points);
        tier = ''
        tierName = ''

        if reward is not None:
            tier = reward["tier"]
            tierName = reward["rewardName"]

        nextReward = self.findNextTier(db, points);
        nextTier = nextReward["tier"]
        nextTierName = nextReward["rewardName"]

        nextTierProgress = self.findProgress(points, nextReward["points"])

        query = {"email": email, "points": points, "tier": tier, "tierName": tierName, "nextTier": nextTier, "nextTierName": nextTierName, "nextTierProgress": nextTierProgress}
        return query

    @coroutine
    def post(self):
        """
        TODO: Post customer to database.

        Get the email and total spent from input argument.
        If it is a new customer insert new customer otherwise update the customer.
        """

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        email = self.get_argument("email")
        total = float(self.get_argument("total"))

        #turn total into points
        points = int(math.floor(total))

        #check if email exsists or not in customer collection
        findEmailQuery = {"email": email}
        myCustomer = db.orders.find_one(findEmailQuery)

        if myCustomer is None:
            #create new customer
            newCustomer = self.createQuery(db, points, email)
            db.orders.insert_one(newCustomer)
        else:
            #get the points & add to points | update customer
            points = points + myCustomer["points"]
            updateCustomer = self.createQuery(db, points, email)
            db.orders.update_one(findEmailQuery, {"$set" : updateCustomer})
