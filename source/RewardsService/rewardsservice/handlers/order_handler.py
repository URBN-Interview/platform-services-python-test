import json
import math

import tornado
from mongo.mongo_manager import MongoManager
from tornado.gen import coroutine
from model.customer import Customer
from util.logger_util import loggingUtil
from util.server_error import UnknownError
from util.server_error import ServerError


class OrderHandler(tornado.web.RequestHandler):
    logger = loggingUtil.get_module_logger(__name__)
    error = None

    @coroutine
    def post(self):
        presentReward = None
        nextReward = None

        data = tornado.escape.json_decode(self.request.body)
        email = data['email']
        orderTotal = data['orderTotal']
        customerExist, isSuccess = MongoManager.getCustomerByEmail(email)
        rewardPoints = math.floor(float(orderTotal))

        if isSuccess:
            if customerExist:
                rewardPoints += customerExist['rewardPoints']
        else:
            OrderHandler.logger.error("Exception block")
            self.set_status(503)
            self.error = SystemError("MongoDB Connection","getCustomerByEmail")
            raise Exception(self.error.type)

        presentRewardList, presentRewardSuccess = MongoManager.getRewardTierByTotalRewardPoints(int(rewardPoints))
        nextRewardList, nextRewardSuccess = MongoManager.getNextRewardTierByTotalRewardPoints(int(rewardPoints))

        customer = Customer(email, rewardPoints)

        if presentRewardSuccess and len(presentRewardList) > 0:
            presentReward = presentRewardList[0]
            customer.setReward(presentReward['tier'], presentReward['rewardName'], rewardPoints)

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

        result, isSuccess = MongoManager.getCustomerByEmail(email)
        if isSuccess:
            self.write(json.dumps(result))

    def write_error(self, status_code, **kwargs):
        if not status_code is None:
            self.set_status(status_code)
        if status_code in [400, 403, 404, 500, 503]:
            if not self.error:
                self.error = UnknownError()
            self.write({"type": self.error.type, "context": self.error.context, "error": self.error.error})
