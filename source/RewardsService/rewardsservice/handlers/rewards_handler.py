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


class Init(tornado.web.RequestHandler):
    def get(self):
        self.write({'message':'hello world'})

class CustomerData(tornado.web.RequestHandler):

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



    @coroutine #async function
    def post(self):
        # client = MongoClient("mongodb", 27017)
        # create cusomer database
        # db = client["Customer"]

        customerInfo = json.loads(self.request.body.decode('utf-8')) # {'email': 'xx', 'order-total': 'xxx'}
        # email = customerInfo['e-mail']
        orderTotal = customerInfo['order-total']
        rewardsTier = self.tier(float(orderTotal))

        # db = client["Rewards"]
        # rewards = list(db.rewards.find({''}, {"_id": 0}))
        # self.write(json.dumps(rewards))

        # rewardPoints =
        # rewardTier =

        #inserts the customer in the 'customer' collection
        # customers = db.customers.insert({"email": email, 'order-total': orderTotal, })

        # data

        self.write({"tier": rewardsTier})
        # self.write({'email': customerInfo['e-mail'], 'orderTotal': customerInfo['order-total'] })



