import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
from rewardsservice.customer_utils import to_reward_points, is_email_valid


class SingleCustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        try:
            client = MongoClient("mongodb", 27017)          #refactor to pass in db connection as dict in url_patterns?
            db = client["Rewards"]
            customerEmail = self.get_argument("email")
            customer = list(db.customers.find({"email": customerEmail}, {"_id": 0}))


            if customer:
                self.write(json.dumps(customer))
            else:
                self.write(json.dumps("<html><body>Sorry, that email was not recognized</body></html>"))

        except Exception as e:
            self.write(json.dumps({'status':'error','error':str(e)}))

    

    @coroutine
    def post(self):
        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            rewards = list(db.rewards.find({}, {"_id": 0}))
            email = self.get_argument("email")
            orderTotal = self.get_argument("orderTotal")

            
            if is_email_valid(email):

                customer = db.customers.find_one({"email": email })
                points = to_reward_points(orderTotal)
              
                if customer:
                    totalPoints = customer["points"] + points
                    customerData = get_tier(rewards, totalPoints, email)
                    
                    db.customers.update_one(customer, {"$set": customerData})
                else:
                    customerData = get_tier(rewards, points, email)
                    
                    db.customers.insert_one(customerData)
        
                customers = list(db.customers.find({}, {"_id": 0}))
                self.write(json.dumps(customers))

            else:
                self.write(json.dumps("<html><body>Please enter a valid email</body></html>")) 


        except Exception as e:
            self.write(json.dumps({'status':'error','error':str(e)}))




#move out of customer_utils due to async/traceback issues
#gen.coroutine for async only!
def get_tier(rewards, points, email):
    
    length = len(rewards)-1
    customerTier = {}

    
    for i in range(length):
        
        if rewards[i]["points"] <= points < rewards[i+1]["points"]:

            progress = get_percent(points, rewards[i]["points"])
            
            customerTier = {
                "email": email,
                "points": points,
                "rewardTier": rewards[i]["tier"],
                "rewardTierName": rewards[i]["rewardName"],
                "nextTier": rewards[i+1]["tier"],
                "nextTierName": rewards[i+1]["rewardName"], 
                "nextTierProgress": progress
            }
        
        elif points < rewards[0]["points"]:
            progress = get_percent(points, 0)
            
            customerTier = {
                "email": email,
                "points": points,
                "rewardTier": "",
                "rewardTierName": "",
                "nextTier": rewards[i]["tier"],
                "nextTierName": rewards[i]["rewardName"], 
                "nextTierProgress": progress
            }

        elif points >= rewards[length]["points"]:

            customerTier = {
                "email": email,
                "points": points,
                "rewardTier": rewards[i]["tier"],
                "rewardTierName": rewards[i]["rewardName"],
                "nextTier": "",
                "nextTierName": "", 
                "nextTierProgress": ""
                }

    return customerTier

    


def get_percent(orderTotal, tierPoints):
    percent =  round((orderTotal/ (100 + tierPoints) ) * 100.0, 2)
   
    return "{} %".format(percent)
