import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))

class OrderHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self, keys):
        #Connect to the database and make two new collections. One collection called Orders and the other called Customer
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        orderCollection = db["Orders"]
        customerCollection = db["Customers"]

        #Accept the parameters passed in by the user
        email = self.get_argument("email", "default")
        orderTotal = self.get_argument("orderTotal", "default")

        #Add the order passed in by the user to the Users collection
        newOrder = {"email": email, "orderTotal": orderTotal}
        orderCollection.insert_one(newOrder)

        #Pull a list of all the orders related to the email submitted and return to the sum of those orders for the purpose of finding the total dollar amount spent
        query = {"email": email}
        listOfOrders = list(orderCollection.find(query))
        totalSpent = 0
        for order in listOfOrders:
            totalSpent += float(order.get("orderTotal"))
            print('TOTAL SPENT')
            print(totalSpent)

        #Use the methods below to find the relevent reward tiers
        currentRewardTier = db.rewards.find_one({"tier": self.findCurrentRewardTier(totalSpent)})
        nextRewardTier = db.rewards.find_one({"tier": self.findNextRewardTier(totalSpent)})

        #Determine the format of the entry based on the dollar amount spent/points
        if totalSpent >= 1000:
            customer =  {"email": email, "rewardPoints": int(totalSpent), "rewardTier": currentRewardTier.get("tier"), "rewardTierName": currentRewardTier.get("rewardName"), "nextRewardTier": "", "nextRewardTierName": "", "nextRewardTierProgress": ""}
        elif totalSpent < 100:
            customer =  {"email": email, "rewardPoints": int(totalSpent), "rewardTier": "", "rewardTierName": "", "nextRewardTier": nextRewardTier.get("tier"), "nextRewardTierName": nextRewardTier.get("rewardName"), "nextRewardTierProgress": ""}
        else:
            customer =  {"email": email, "rewardPoints": int(totalSpent), "rewardTier": currentRewardTier.get("tier"), "rewardTierName": currentRewardTier.get("rewardName"), "nextRewardTier": nextRewardTier.get("tier"), "nextRewardTierName": nextRewardTier.get("rewardName"), "nextRewardTierProgress": ""}

        #Lookup the customer to see if they already have an entry in the collection. If they do not, add them to the collection, if they do, update their record
        customerLookup = customerCollection.find_one(query)
        if customerLookup is None:
            customerCollection.insert_one(customer)
        else:
            newValues = {"$set": customer}
            customerCollection.update_one({"_id": customerLookup.get("_id")}, newValues)

        testAddCustomer = customerCollection.find_one(query)
        print("test add")
        print(testAddCustomer)         
            

    def findCurrentRewardTier(self, totalSpent):
        if totalSpent >= 1000:
            return "J"
        elif totalSpent >= 900 and totalSpent <1000:
            return "I"
        elif totalSpent >= 800 and totalSpent < 900:
            return "H"
        elif totalSpent >= 700 and totalSpent < 800:
            return "G"
        elif totalSpent >= 600 and totalSpent < 700:
            return "F"
        elif totalSpent >= 500 and totalSpent < 600:
            return "E"
        elif totalSpent >= 400 and totalSpent < 500:
            return "D"
        elif totalSpent >= 300 and totalSpent < 400:
            return "C"
        elif totalSpent >= 200 and totalSpent < 300:
            return "B"
        elif totalSpent >= 100 and totalSpent < 200:
            return "A"
        elif totalSpent < 100:
            return ""

    def findNextRewardTier(self, totalSpent):
        if totalSpent >= 1000:
            return "J"
        elif totalSpent >= 900 and totalSpent < 1000:
            return "J"
        elif totalSpent >= 800 and totalSpent < 900:
            return "I"
        elif totalSpent >= 700 and totalSpent < 800:
            return "H"
        elif totalSpent >= 600 and totalSpent < 700:
            return "G"
        elif totalSpent >= 500 and totalSpent < 600:
            return "F"
        elif totalSpent >= 400 and totalSpent < 500:
            return "E"
        elif totalSpent >= 300 and totalSpent < 400:
            return "D"
        elif totalSpent >= 200 and totalSpent < 300:
            return "C"
        elif totalSpent >= 100 and totalSpent < 200:
            return "B"
        elif totalSpent < 100:
            return "A"

class CustomerHandler(tornado.web.RequestHandler):

    #Gets all customers
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customerCollection = db["Customers"]
        customers = list(db.rewards.customerCollection.find())
        self.write(json.dumps(customers))

class CustomerDataHandler(tornado.web.RequestHandler):

    #Accepts an email address and returns the rewards data
    @coroutine
    def get(self, keys):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customerCollection = db["Customers"]
        email = self.get_argument("email", "default")
        query = {"email": email}
        customer = list(customerCollection.find_one(query))

