import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


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

            email = self.get_argument("email")
            orderTotal = self.get_argument("orderTotal")

             
            #TO DO util funcs: 
                # is_email: Validate email as email
                # to_reward_points: convert orderTotal to reward points 
                # get_next_tier: calcuate percent to next tier, next tier and name 
            


            points = to_reward_points(orderTotal)
            reward = db.rewards.find({"points": points}, {"_id": 0})    #python object destructuring? (dictionaries)
            
            db.customer.insert({"email": email, "rewardPoints": orderTotal})
    
        except Exception as e:
            self.write(json.dumps({'status':'error','error':str(e)}))
