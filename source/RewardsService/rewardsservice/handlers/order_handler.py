import tornado.web
import json
import math

from util.validation import Validaton
from pymongo import MongoClient
from tornado.gen import coroutine
from tornado.options import options
from model.customer import Customer
from util.server_error import DatabaseError

class OrderHandler(tornado.web.RequestHandler):
    customerClient = 'Customers'
    rewardsClient = 'Rewards'
    error =  None

    @coroutine
    def post(self):
        client = MongoClient(options.mongodb_host)
        customerDb = client[self.customerClient]
        rewardsDb = client[self.rewardsClient]

        email = str(self.get_argument('email', ''))
        orderTotal = str(self.get_argument('orderTotal', ''))

        validateError = Validaton().emailValidation(email, 'email').currencyValidation(orderTotal, 'orderType').validate()
        
        if validateError:
            self.error = validateError
            raise Exception(self.error.type)

        customerExist = customerDb.customers.find_one({'email': email}, {'_id': 0})
        if(customerExist):
            self.error = DatabaseError('Customer already exist')
            raise Exception(self.error.type)

        customer = Customer(email, float(orderTotal))
        dallor = int(orderTotal.split('.')[0])
        currentReward = None
        nextReward = None

        for reward in list(rewardsDb.rewards.find({}, {'_id': 0})):
            if(dallor < reward['points']):
                nextReward = reward
                break

            currentReward = reward

        if(currentReward):
            customer.setReward(currentReward['tier'], currentReward['rewardName'])

        if(nextReward):
            customer.setNextReward(nextReward['tier'], nextReward['rewardName'])
            currentRewardPoints = 0
            if(currentReward):
                currentRewardPoints = currentReward['points']
            customer.tierProgress = (dallor - currentRewardPoints)/(nextReward['points'] - currentRewardPoints)
            
        customerDb.customers.insert({'email': customer.email, 'orderTotal': customer.orderTotal, 'rewardTier': customer.rewardTier, 'rewardName': customer.rewardName, 'nextRewardTier': customer.nextRewardTier, 'nextRewardName': customer.nextRewardName, 'nextRewardProgress': customer.tierProgress})
        createdCustomer = customerDb.customers.find_one({'email': email}, {'_id': 0})
        self.write(json.dumps(createdCustomer))

    def write_error(self, status_code, **kwargs):
        if status_code == 500 and self.error:
            self.write({"type" : self.error.type, "context": self.error.context})
        elif status_code == 500:
            self.write({'message: Unknown Error'})