import json
import math

import tornado
from mongo.mongo_manager import MongoManager
from tornado.gen import coroutine
from model.customer import Customer


class OrderHandler(tornado.web.RequestHandler):
    @coroutine
    def post(self):
        presentReward = None
        nextReward = None
        # Getting request data
        email = str(self.get_argument('email', ''))
        orderTotal = str(self.get_argument('orderTotal', ''))

        customerExist, isSuccess = MongoManager.getCustomer(email)
        rewardPoints = math.floor(float(orderTotal))

        if isSuccess:
            if customerExist:
                rewardPoints += customerExist['rewardPoints']
        else:
            self.write_error(self, 503, "Please try again after some time")

        presentRewardList, presentRewardSuccess = MongoManager.getRewardTierByTotalRewardPoints(int(rewardPoints))
        nextRewardList, nextRewardSuccess = MongoManager.getNextRewardTierByTotalRewardPoints(int(rewardPoints))

        customer = Customer(email, rewardPoints)


        print("len(presentRewardList")
        print(len(presentRewardList))

        if presentRewardSuccess and len(presentRewardList) > 0:
            presentReward = presentRewardList[0]
            customer.setReward(presentReward['tier'], presentReward['rewardName'], rewardPoints)

        print("len(nextRewardList")
        print(len(nextRewardList))
        if nextRewardSuccess and len(nextRewardList) > 0:
            nextReward = nextRewardList[0]
            customer.setNextReward(nextReward['tier'], nextReward['rewardName'])
        else:
            customer.setNextReward('None', 'None')

        if presentRewardSuccess and nextRewardSuccess and nextReward is not None:
            currentRewardPoints = 0
            if presentReward:
                currentRewardPoints = presentReward['points']
                nextRewardPoints = nextReward['points']
            customer.tierProgress = (rewardPoints - currentRewardPoints) / (nextReward['points'] - currentRewardPoints)

        if customerExist:
            MongoManager.updateCustomer(customer)
        else:
            MongoManager.insertCustomer(customer)
            self.set_status(201)

        result = list(MongoManager.getCustomer(email))
        self.write(json.dumps(result))
