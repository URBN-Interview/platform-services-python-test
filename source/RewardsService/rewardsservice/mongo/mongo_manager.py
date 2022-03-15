import logging

import pymongo

from pymongo import MongoClient

from util.logger_util import loggingUtil


class MongoManager:
    customerDb = 'Customers'
    rewardsDb = 'Rewards'
    logger = loggingUtil.get_module_logger(__name__)

    class __MongoManager:
        def __init__(self):
            # Initialise mongo client
            self.client = MongoClient('mongodb', 27017)

    __instance = None

    def get_module_logger(mod_name):
        logger = logging.getLogger(mod_name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def __init__(self):
        if not MongoManager.__instance:
            MongoManager.__instance = MongoManager.__MongoManager()

    def __getattr__(self, item):
        return getattr(self.__instance, item)

    def getCustomerByEmail(email):
        isSuccess = True
        customer = None
        try:
            client = MongoManager().client
            db = client[MongoManager.customerDb]
            customer = db.customers.find_one({'email': email}, {'_id': 0})
        except Exception as e:
            isSuccess = False
            MongoManager.logger.error("Mongo connection Exception in getCustomerByEmail ", e)
        finally:
            MongoManager.logger.error("Keeping connection open as using singleton bean")
        return customer, isSuccess

    def getCustomers(self):
        isSuccess = False
        customers = None
        try:
            client = MongoManager().client
            db = client[MongoManager.customerDb]
            customers = list(db.customers.find({}, {"_id": 0}))
            isSuccess = True
        except Exception as e:
            MongoManager.logger.error("Mongo connection Exception in getCustomers ", e)
        finally:
            MongoManager.logger.error("Keeping connection open as using singleton bean")
        return customers, isSuccess

    @staticmethod
    def getRewardTierByTotalRewardPoints(total):
        isSuccess = False
        reward = None
        try:
            MongoManager.logger.error(total)
            client = MongoManager().client
            db = client["Rewards"]
            reward = list(
                db.rewards.find({'points': {'$lte': total}}, {"_id": 0}).limit(1).sort("points", pymongo.DESCENDING))
            isSuccess = True
        except Exception as e:
            MongoManager.logger.error("Mongo connection Exception in getNextRewardTierByTotalRewardPoints ", e)
        finally:
            MongoManager.logger.error("Keeping connection open as using singleton bean")
        return reward, isSuccess

    @staticmethod
    def getNextRewardTierByTotalRewardPoints(total):
        isSuccess = False
        reward = None
        try:
            client = MongoManager().client
            db = client["Rewards"]
            reward = list(
                db.rewards.find({'points': {'$gt': total}}, {"_id": 0}).limit(1).sort("points", pymongo.ASCENDING))

            isSuccess = True
        except Exception as e:
            MongoManager.logger.error("Mongo connection Exception in getNextRewardTierByTotalRewardPoints ", e)
        finally:
            MongoManager.logger.info("Keeping connection open as using singleton bean")
        return reward, isSuccess

    def updateCustomer(customer):
        isSuccess = False
        response = None
        try:
            client = MongoManager().client
            customerDb = client[MongoManager.customerDb]
            response = customerDb.customers.update({'email': customer.email},
                                                   {'email': customer.email, 'rewardPoints': customer.rewardPoints,
                                                    'rewardTier': customer.rewardTier,
                                                    'rewardName': customer.rewardName,
                                                    'nextRewardTier': customer.nextRewardTier,
                                                    'nextRewardName': customer.nextRewardName,
                                                    'nextRewardProgress': customer.tierProgress})
            isSuccess = True
        except Exception as e:
            MongoManager.logger.error("Mongo connection failure updateCustomer", e)
        finally:
            MongoManager.logger.error("Keeping connection open as using singleton bean")
        return response, isSuccess

    def insertCustomer(customer):
        isSuccess = False
        response = None
        try:
            client = MongoManager().client
            customerDb = client[MongoManager.customerDb]
            response = customerDb.customers.insert(
                {'email': customer.email, 'rewardPoints': customer.rewardPoints, 'rewardTier': customer.rewardTier,
                 'rewardName': customer.rewardName, 'nextRewardTier': customer.nextRewardTier,
                 'nextRewardName': customer.nextRewardName, 'nextRewardProgress': customer.tierProgress})
            isSuccess = True
        except Exception as e:
            MongoManager.logger.error("Mongo connection failure getCustomerByEmail", e)
        finally:
            MongoManager.logger.error("Keeping connection open as using singleton bean")
        return response, isSuccess
