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

    @coroutine #async function
    def post(self):
        # client = MongoClient("mongodb", 27017)
        # db = client["Customer"]
        # db.customers.insert({"Email": })
        customerInfo = json.loads(self.request.body.decode('utf-8'))
        self.write({'email': customerInfo['e-mail'], 'orderTotal': customerInfo['order-total'] }, )
        # self.write({'orderTotal': customerInfo['order-total']})
        # self.write({'order total': json.loads(self.request.body)})


