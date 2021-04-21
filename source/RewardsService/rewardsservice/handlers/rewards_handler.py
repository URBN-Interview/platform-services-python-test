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
        
        customer_submitteddata= {"email": self.get_body_argument("email"),"OrderTotal":self.get_body_argument("ordertotal") } #for Endpoint 1 requirement 3
    
        customer_fulldata=[] #making an empty list 
        customer_fulldata.append(customer_submitteddata.copy()) #storing dict into list 
       

        client = MongoClient("mongodb",27017)
        db = client["Rewards"]
        querycustomerrewards= list(db.rewards.find( { "points": self.customer_rewardcalc(self.get_body_argument("ordertotal"))}, { "tier" : 1, "rewardName" : 1, "_id":0 } ))#for Endpoint 1 requirement 4
        self.write(dumps((self.customer_rewardcalc(self.get_body_argument("ordertotal")))))
        self.write('<br>')

        customer_fulldata.append(querycustomerrewards) #storing into list 
        querryfuturerewards=  list(db.rewards.find( { "points": self.customer_rewardcalc(self.get_body_argument("ordertotal"))*1000}, { "tier" : 1, "rewardName" : 1, "_id":0 } )) #for Endpoint 1 requirement 5,6,7
        self.write(dumps(self.customer_rewardcalc(self.get_body_argument("ordertotal"))+100))


        customer_fulldata.append(querryfuturerewards)
        customer_PercentProgress = {"NextTierProgress": self.customer_RewardProgress(self.get_body_argument("ordertotal"))} #for Endpoint 1 requirement 8
        customer_fulldata.append(customer_PercentProgress.copy())
        self.write('<br>')
        self.write(dumps(self.customer_RewardProgress(self.get_body_argument("ordertotal"))))
        #self.write(dumps(customer_fulldata))



        #mongoinsert = db.customer.insert(customer_dict)
        #mongoretrieve = list(db.customer.find({}, {"_id": 0}))
        #self.write(json.dumps(mongoretrieve))

