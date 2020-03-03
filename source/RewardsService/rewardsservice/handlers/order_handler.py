import tornado.web
import json
import math

from util.validation import Validaton
from pymongo import MongoClient
from tornado.gen import coroutine
from tornado.options import options
from model.customer import Customer

class OrderHandler(tornado.web.RequestHandler):
    customerClient = 'Customers'
    rewardsClient = 'Rewards'

    @coroutine
    def post(self):
        client = MongoClient(options.mongodb_host)
        customerDb = client[self.customerClient]
        rewardsDb = client[self.rewardsClient]

        email = str(self.get_argument('email', ''))
        orderTotal = str(self.get_argument('orderTotal', ''))
        Validaton().emailValidation(email).currencyValidation(orderTotal).validate()
        
        customerExist = customerDb.customers.find_one({'email': email}, {'_id': 0})
        if(customerExist):
            raise Exception('Customer already exist')

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

        if(nextReward):
            currentRewardPoints = 0
            if(currentReward):
                currentRewardPoints = currentReward['points']
            customer.tierProgress = (dallor - currentRewardPoints)/(nextReward['points'] - currentRewardPoints)

        customerDb.customers.insert({'email': customer.email, 'orderTotal': customer.orderTotal, 'rewardTier': customer.rewardTier, 'rewardName': customer.rewardName, 'nextRewardTier': customer.nextRewardTier, 'nextRewardName': customer.nextRewardName, 'nextRewardTierProgress': customer.tierProgress})
        createdCustomer = customerDb.customers.find_one({'email': email}, {'_id': 0})
        self.write(json.dumps(createdCustomer))