import tornado.web
import json
import math


from util.server_error import UnknownError
from util.validation import Validaton
from pymongo import MongoClient
from tornado.gen import coroutine
from tornado.options import options
from model.customer import Customer

class OrderHandler(tornado.web.RequestHandler):
    customerClient = 'Customers'
    rewardsClient = 'Rewards'
    error =  None

    @coroutine
    def get(self):
        client = MongoClient(options.mongodb_host)
        customerDb = client[self.customerClient]
        rewardsDb = client[self.rewardsClient]
        currentReward = None
        nextReward = None

        email = str(self.get_argument('email', ''))
        orderTotal = str(self.get_argument('orderTotal', ''))

        validateError = Validaton().emailValidation(email, 'email').currencyValidation(orderTotal, 'orderType').validate()
        
        if validateError:
            self.error = validateError
            raise Exception(self.error.type)

        customerExist = customerDb.customers.find_one({'email': email}, {'_id': 0})
        dallor = int(orderTotal.split('.')[0])

        if(customerExist):
            dallor += customerExist['rewardPoints']

        customer = Customer(email, float(orderTotal))

        for reward in list(rewardsDb.rewards.find({}, {'_id': 0})):
            if(dallor < reward['points']):
                nextReward = reward
                break

            currentReward = reward

        if(currentReward):
            customer.setReward(currentReward['tier'], currentReward['rewardName'], currentReward['points'])

        if(nextReward):
            customer.setNextReward(nextReward['tier'], nextReward['rewardName'])
            currentRewardPoints = 0
            if(currentReward):
                currentRewardPoints = currentReward['points']
            customer.tierProgress = (dallor - currentRewardPoints)/(nextReward['points'] - currentRewardPoints)
            
        
        if(customerExist):
            customerDb.customers.update({'email': customer.email}, {'email': customer.email, 'rewardPoints': dallor, 'rewardTier': customer.rewardTier, 'rewardName': customer.rewardName, 'nextRewardTier': customer.nextRewardTier, 'nextRewardName': customer.nextRewardName, 'nextRewardProgress': customer.tierProgress})
        else:    
            customerDb.customers.insert({'email': customer.email, 'rewardPoints': dallor, 'rewardTier': customer.rewardTier, 'rewardName': customer.rewardName, 'nextRewardTier': customer.nextRewardTier, 'nextRewardName': customer.nextRewardName, 'nextRewardProgress': customer.tierProgress})
        
        result = list(customerDb.customers.find({'email': email}, {'_id': 0}))
        self.write(json.dumps(result))

    def write_error(self, status_code, **kwargs):
        if status_code in [400, 403, 404, 500, 503]:
            if not self.error:
                self.error = UnknownError()
            self.write({"type" : self.error.type, "context": self.error.context, "error": self.error.error})