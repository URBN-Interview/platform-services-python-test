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
            totalSpent += int(order.get("orderTotal"))

        #Use the findRewardTiers method below to find the relevent reward tiers
        rewardTiers = self.findRewardTiers(totalSpent)
        returnedTiers = db.rewards.find({"$or": [{"tier": rewardTiers[0]}, {"tier": rewardTiers[1]}]}).sort("points", 1)

        #Use the same query to determine if the customer's email already exists in the collection. 
        customer = customerCollection.find_one(query)
        if customer is None:
            customer = {"email": email, "rewardPoints": int(totalSpent), "rewardTier": "", "rewardTierName": "", "nextRewardTier": "", "nextRewardTierName": "", "nextRewardTierProgress": ""}
            customerCollection.insert_one(customer)
        

    def findRewardTiers(self, totalSpent):
        if totalSpent >= 1000:
            return list(["J","J"])
        elif totalSpent >= 800 and totalSpent < 900:
            return list(["H","I"])
        elif totalSpent >= 700 and totalSpent < 800:
            return list(["G","H"])
        elif totalSpent >= 600 and totalSpent < 700:
            return list(["F","G"])
        elif totalSpent >= 500 and totalSpent < 600:
            return list(["E","F"])
        elif totalSpent >= 400 and totalSpent < 500:
            return list(["D","E"])
        elif totalSpent >= 300 and totalSpent < 400:
            return list(["C","D"])
        elif totalSpent >= 200 and totalSpent < 300:
            return list(["B","C"])
        elif totalSpent >= 100 and totalSpent < 200:
            return list(["A","B"])
        elif totalSpent < 100:
            return list(["", "A"])

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
        customer = list(customerCollection.find(query))

