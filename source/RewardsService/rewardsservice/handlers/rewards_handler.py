import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
from bson.json_util import dumps, loads #using this to load data more clearly 


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))


#creating this class to accept  a customer's data
class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/response" method="POST">'
                    '<label for="email"> Customer Email address: </label>'
                    '<input type="text" id="email" name="email"><br>'
                    '<label for="ordertotal">Customer Order Total: </label>'
                    '<input type="text" id="ordertotal" name="ordertotal"><br>'
                    '<br><input type="submit" value="Submit">'
                    '</form></body></html>')




    def post(self):
        client = MongoClient("mongodb",27017)
        db = client["Rewards"]
        customer_submitteddata= {"email": self.get_body_argument("email"),"OrderTotal":self.get_body_argument("ordertotal") }
        customer_fulldata=[]
        customer_fulldata.append(customer_submitteddata.copy())
        querycustomerrewards= list(db.rewards.find( { "points": 100 }, { "tier" : 1, "rewardName" : 1, "_id":0 } ))
        customer_fulldata.append(querycustomerrewards)
        self.write(dumps(customer_fulldata))


        #mongoinsert = db.customer.insert(customer_dict)
        #mongoretrieve = list(db.customer.find({}, {"_id": 0}))
        #self.write(json.dumps(mongoretrieve))

