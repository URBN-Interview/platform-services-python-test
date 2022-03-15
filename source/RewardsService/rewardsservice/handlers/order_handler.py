import json
import math

import tornado
from mongo.mongo_manager import MongoManager
from tornado import web
from tornado.gen import coroutine
from model.customer import Customer
from util.logger_util import loggingUtil
from util.server_error import UnknownError
from util.server_error import ServerError
from util.validator import Validator


class OrderHandler(tornado.web.RequestHandler):
    logger = loggingUtil.get_module_logger(__name__)
    error = None

    @coroutine
    def post(self):
        presentReward = None
        nextReward = None

        # Getting params from request
        data = tornado.escape.json_decode(self.request.body)
        email = data['email']
        orderTotal = data['orderTotal']

        # validating the request parameters
        isValidEmail = Validator().emailValidation(email, 'email')
        if not isValidEmail:
            self.error = ServerError("InvalidRequestParams", "Invalid email address or email Address is missing in request body")
            raise web.HTTPError(400)

        if orderTotal is None or not orderTotal.isnumeric():
            self.error = ServerError("InvalidRequestParams", "Order total should be numeric ")
            raise web.HTTPError(400)

        customerExist, isSuccess = MongoManager.getCustomerByEmail(email)
        rewardPoints = math.floor(float(orderTotal))

        if isSuccess:
            if customerExist:
                rewardPoints += customerExist['rewardPoints']
        else:
            self.error = ServerError("ServiceUnavailable", "Please try again after some time")
            raise web.HTTPError(503)

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
        else:
            self.error = ServerError("ServiceUnavailable", "Please try again after some time")
            raise web.HTTPError(503)

    def write_error(self, status_code, **kwargs):
        if status_code in [400, 403, 404, 500, 503]:
            if not self.error:
                self.error = UnknownError()
            self.write({"type": self.error.type, "context": self.error.context, "error": self.error.error})
