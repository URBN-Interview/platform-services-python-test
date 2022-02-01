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

# Insert a customer's email and order number
# http://localhost:7050/insert?email=test@gmail&order=100
class InsertHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        #Arguments
        email = str(self.get_argument("email"))
        total = float(self.get_argument("total"))
        pointsReward = int(total) #round down

        #Call to DB and retrieve the list of rewards and orders
        client = MongoClient("mongodb", 27017)
        rewards_db = client["Rewards"]
        order_db = client["Orders"]
        rewardsList = list(rewards_db.rewards.find({}, {"_id": 0}))
        orderList = list(order_db.orders.find({}, {"_id": 0}))

        #Base case: Is the order list empty? If so insert a new entry, if not modify the given customer account
        if(len(orderList) == 0):
            if(pointsReward < 100):
                index = 0
            elif(pointsReward >= 100 and pointsReward < 1000):
                pointStr = str(pointsReward)
                index = int(pointStr[0]) - 1
            else:
                index = 9
            curr = rewardsList[index]
            next = rewardsList[index+1]
            progress =  pointsReward / curr["points"]
            if(progress > 1):
                progress = 100 / progress
            order_db.orders.insert({"email": email, "points": pointsReward, "currTier": curr["tier"], "currReward": curr["rewardName"], "nextTier": next["tier"], "nextReward": next["rewardName"], "progress": progress})
        else:
            didUpdate = 0
            for i in orderList:
                if(i["email"] == email):
                    pointsReward = pointsReward + i["points"]
                    if(pointsReward < 100):
                        index = 0
                    elif(pointsReward >= 100 and pointsReward < 1000):
                        pointStr = str(pointsReward)
                        index = int(pointStr[0]) - 1
                    else:
                        index = 9
                    curr = rewardsList[index]
                    next = rewardsList[index+1]
                    progress =  pointsReward / curr["points"]
                    if(progress > 1):
                        progress = 100 / progress
                    updatedValues = { "$set": {"email": email, "points": pointsReward, "currTier": curr["tier"], "currReward": curr["rewardName"], "nextTier": next["tier"], "nextReward": next["rewardName"], "progress": progress}}
                    order_db.orders.update_one(i, updatedValues)
                    didUpdate = 1

            #If the list was not empty and the email was not in the list, insert a new instance
            if(didUpdate == 0):
                if(pointsReward < 100):
                    index = 0
                elif(pointsReward >= 100 and pointsReward < 1000):
                    pointStr = str(pointsReward)
                    index = int(pointStr[0]) - 1
                else:
                    index = 9
                curr = rewardsList[index]
                next = rewardsList[index+1]
                progress =  pointsReward / curr["points"]
                if(progress > 1):
                    progress = 100 / progress
                order_db.orders.insert({"email": email, "points": pointsReward, "currTier": curr["tier"], "currReward": curr["rewardName"], "nextTier": next["tier"], "nextReward": next["rewardName"], "progress": progress})

        #Return the updated list of orders
        updatedOrders = list(order_db.orders.find({}, {"_id": 0}))
        self.write(json.dumps(updatedOrders))

# Return the data associated with a customer email
# http://localhost:7050/find?email=test@gmail.com
class CustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        email = self.get_argument("email")

        client = MongoClient("mongodb", 27017)
        db = client["Orders"]
        orders = list(db.orders.find({}, {"_id": 0}))

        #self.write("Email is: " + email)

        output = []
        for i in orders:
            if(i["email"] == email):
                output.append(i)

        if(output != []):
            self.write(json.dumps(output))
        #else:
            #self.write("Email not found!")

# Return the entire list of orders
# http://localhost:7050/all
class AllHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Orders"]
        orders = list(db.orders.find({}, {"_id": 0}))
        self.write(json.dumps(orders))

# Clear the list of orders. Helper function to make testing easier.
# http://localhost:7050/clear
class ClearHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Orders"]
        db.orders.remove()
        orders = list(db.orders.find({}, {"_id": 0}))
        self.write('Cleared! See ->' + json.dumps(orders))
