import json	
import tornado.web	
import math	

from pymongo import MongoClient	
from pymongo import MongoClient	
from tornado.gen import coroutine	
from tornado.options import options	
from model.customer import Customers	

class OrderHandler(tornado.web.RequestHandler):	

    @coroutine	
    def post(self):	
        client = MongoClient(options.mongodb_host)	
        customerDb = client["Customers"]	
        rewardsDb = client["Rewards"]	
        currentReward = None	
        nextReward = None	

        email = self.get_argument('email', '')	
        orderTotal = self.get_argument('orderTotal', '')	

        # Todo, can put backend email validation here	
        oldCustomer = customerDb.customers.find_one({"email": email}, {'_id':0})	

        # 1$ = 1 points (has to be int)	
        dollar = int(orderTotal)	


        # check customer info against DB	
        if(oldCustomer):	
            dollar += oldCustomer['points']	
        customer = Customers(email, int(orderTotal))	
        print(customer)	

            # for loop to find corresponding rewards in RewardsDB	

        for reward in list(rewardsDb.rewards.find({}, {"_id": 0})):	
            if(dollar < reward["points"]):	
                    nextReward = reward	

                    break	
            currentReward = reward	

        # Get current reward status	
        if(currentReward):	
            customer.currentReward(currentReward["tier"], currentReward['rewardName'], currentReward['points'])	

        # Get next reward status	
        if(nextReward):	
            # print(nextReward)	
            customer.newReward(nextReward["tier"], nextReward["rewardName"], 'progress')	
            # calculate current reward points	
            currentPoints = 0	
            if(currentReward):	
                currentPoints = currentReward['points']	
            customer.progress = currentPoints/nextReward['points']	


        # if customer exist, only update	
        if(oldCustomer):	
            customerDb.customers.update({'email': customer.email},	
            {'email': customer.email, 'points': dollar, 'tier': customer.tier, 'rewardName': customer.rewardName, 'nextTier': customer.nextTier, 'nextReward': customer.nextReward, 'progress': customer.progress})	
            # print(oldCustomer)	
        # else customer is new, insert new customer	
        else:	
            customerDb.customers.insert({'email': customer.email, 'points': dollar, 'tier': customer.tier, 'rewardName': customer.rewardName, 'nextTier': customer.nextTier, 'nextReward': customer.nextReward, 'progress': customer.progress})	

        result = list(customerDb.customers.find({"email": email}, {"_id": 0}))	
        self.write(json.dumps(result))	

# error handler	
    def write_error(self, status_code, **kwargs):	
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:	
            # in debug mode, try to send a traceback	
            self.set_header("Content-Type", "text/plain")	
            for line in traceback.format_exception(*kwargs["exc_info"]):	
                self.write(line)	
            self.finish()	
        else:	
            self.finish(	
                "<html><title>%(code)d: %(message)s</title>"	
                "<body>%(code)d: %(message)s</body></html>"	
                % {"code": status_code, "message": self._reason}	
            )