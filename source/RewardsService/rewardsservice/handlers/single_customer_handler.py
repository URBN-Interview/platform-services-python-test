import json
import tornado.web


from pymongo import MongoClient
from tornado.gen import coroutine
from rewardsservice.customer_utils import to_reward_points, get_tier, is_email_valid

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

            
            if is_email_valid(email):

                customer = list(db.customers.find({"email": email }, {"id": 0}))
                points = to_reward_points(orderTotal)
                customerData = get_tier(points, email)

                


                # if customer:
                #     db.customer.update_one(customer, {"email": email, "rewardPoints": points, })
                # else:
                #     db.customer.insert({"email": email, "rewardPoints": orderTotal})
        

                #move to get_tier
                # if points >= 100:
                #     tier = get_tier(points, email)
                #     db.customer.update_one(customer, {*tier})
                # else:
                #     db.customer.update_one(customer, {"rewardPoints": points})

                self.write(json.dumps({'status':204}))

            else:
                self.write(json.dumps("<html><body>Please enter a valid email</body></html>")) 

        except Exception as e:
            self.write(json.dumps({'status':'error','error':str(e)}))
