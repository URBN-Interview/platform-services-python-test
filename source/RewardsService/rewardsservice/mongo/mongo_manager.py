import pymongo

from pymongo import MongoClient


class MongoManager:
    customerDb = 'Customers'
    rewardsDb = 'Rewards'

    class __MongoManager:
        def __init__(self):
            # Initialise mongo client
            self.client = MongoClient('mongodb', 27017)

    __instance = None

    def __init__(self):
        if not MongoManager.__instance:
            MongoManager.__instance = MongoManager.__MongoManager()

    def __getattr__(self, item):
        return getattr(self.__instance, item)

    def getCustomer(email):
        print(email)
        isSuccess = False
        try:
            client = MongoManager().client
            db = client["Customers"]
            # list(db.customers.find({"email": email}, {"_id": 0}))
            customer = db.customers.find_one({'email': email}, {'_id': 0})
            isSuccess = True
        except Exception as e:
            return []
        finally:
            print("Keeping connection open as using singleton bean")
        return customer, isSuccess

    def getCustomers(self):
        isSuccess = False
        try:
            client = MongoManager().client
            db = client["Customers"]
            customers = list(db.customers.find({}, {"_id": 0}))
            print("len(customers)")

            print(len(customers))
            isSuccess = True
        except Exception as e:
            return []
        finally:
            print("Keeping connection open as using singleton bean")
        return customers

    @staticmethod
    def getRewardTierByTotalRewardPoints(total):
        isSuccess = False
        try:
            print(total)
            client = MongoManager().client
            db = client["Rewards"]
            reward = list(
                db.rewards.find({'points': {'$lte': total}}, {"_id": 0}).limit(1).sort("points", pymongo.DESCENDING))
            isSuccess = True
        except Exception as e:
            print(e)
            return []
        finally:
            print("Keeping connection open as using singleton bean")
        return reward, isSuccess

    @staticmethod
    def getNextRewardTierByTotalRewardPoints(total):
        isSuccess = False
        try:
            client = MongoManager().client
            db = client["Rewards"]
            reward = list(
                db.rewards.find({'points': {'$gt': total}}, {"_id": 0}).limit(1).sort("points", pymongo.ASCENDING))
            print(len(reward))
            isSuccess = True
        except Exception as e:
            return []
        finally:
            print("Keeping connection open as using singleton bean")
        return reward, isSuccess

    def updateCustomer(customer):
            isSuccess = False
            try:
                client = MongoManager().client
                customerDb = client["Customers"]
                response = customerDb.customers.update({'email': customer.email},
                                            {'email': customer.email, 'rewardPoints': customer.rewardPoints,
                                             'rewardTier': customer.rewardTier,
                                             'rewardName': customer.rewardName,
                                             'nextRewardTier': customer.nextRewardTier,
                                             'nextRewardName': customer.nextRewardName,
                                             'nextRewardProgress': customer.tierProgress})
                isSuccess = True
            except Exception as e:
                return []
            finally:
                print("Keeping connection open as using singleton bean")
            return response, isSuccess

    def insertCustomer(customer):
            isSuccess = False
            try:
                client = MongoManager().client
                customerDb = client["Customers"]
                response = customerDb.customers.insert(
                    {'email': customer.email, 'rewardPoints': customer.rewardPoints, 'rewardTier': customer.rewardTier,
                     'rewardName': customer.rewardName, 'nextRewardTier': customer.nextRewardTier,
                     'nextRewardName': customer.nextRewardName, 'nextRewardProgress': customer.tierProgress})
                isSuccess = True
            except Exception as e:
                return []
            finally:
                print("Keeping connection open as using singleton bean")
            return response, isSuccess
