import json
import tornado.web
import math
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
    #method for Endpoint 1  requirement 2 
    @staticmethod
    def customer_rewardcalc(x): 
	    x = int(float(x))
	    if (x >= 1000):
		    x == 1000
	    else:
		    x = int(math.ceil(x//100) * 100)	
	    return x
			

    #method for Endpoint 1  requirement 9
  
    @staticmethod
    def customer_RewardProgress(x): 
	    x = int(float(x))
	    if (x >= 1000):
		    x = 0
	    else:
		    x = math.ceil(x//100) * 100
		    x = round((x /(x+100)),2)
	    return x

	
    def post(self):
        
        customer_data= {"email": self.get_body_argument("email"),"OrderTotal":self.get_body_argument("ordertotal") } #for Endpoint 1 requirement 3
    
        client = MongoClient("mongodb",27017)
        db = client["Rewards"]
        querycustomerrewards= db.rewards.find( { "points": self.customer_rewardcalc(self.get_body_argument("ordertotal"))}, { "tier" : 1, "rewardName" : 1, "_id":0 } )#for Endpoint 1 requirement 4
        for x in  querycustomerrewards: 
            customer_data.update(x)
        querryfuturerewards = db.rewards.find( { "points": self.customer_rewardcalc(self.get_body_argument("ordertotal"))+ 100}, { "tier" : 1, "rewardName" : 1, "_id":0 } )
        temp={}  #storing  this query in a temporary dict to extract the data
        for x in  querryfuturerewards: 
            temp.update(x)
        futurerewards=  { "NextPoints": (self.customer_rewardcalc(self.get_body_argument("ordertotal"))+100),  "NextTier" : temp["tier"], "NextRewardName" : temp["rewardName"]}   #append the temporary data into our customer collection
        customer_data.update(futurerewards)
        customer_PercentProgress = {"NextTierProgress": self.customer_RewardProgress(self.get_body_argument("ordertotal"))} #for Endpoint 1 requirement 8
        customer_data.update(customer_PercentProgress)

        self.write(dumps(customer_data))
        self.write("<br>")
        self.write("<br>")
        mongoinsert = db.customer.insert_one(customer_data)
        mongoretrieve = list(db.customer.find({}, {"_id": 0}))
        self.write(json.dumps(mongoretrieve))

