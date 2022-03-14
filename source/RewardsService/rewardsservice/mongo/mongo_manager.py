from pymongo import DESCENDING

from pymongo import MongoClient


class MongoManager:
    class __MongoManager:
        def __init__(self):
            # Initialise mongo client
            self.client = MongoClient('localhost', 27017)

    __instance = None

    def __init__(self):
        if not MongoManager.__instance:
            MongoManager.__instance = MongoManager.__MongoManager()

    def __getattr__(self, item):
        return getattr(self.__instance, item)


    @staticmethod
    def getCustomer(email):
        isSuccess = False
        try:
            client = MongoManager().client
            db = client["Customer"]
            customer = db.find_one({"email": email})
            isSuccess = True
        except Exception as e:
            return []
        finally:
            print("Closing the database")
            # close the database
        return customer,isSuccess

    @staticmethod
    def getCustomers():
        try:
            client = MongoManager().client
            db = client["Customer"]
            customers = db.find()
        except Exception as e:
            return []
        finally:
            print("Closing the database")
            # close the database
        return customers

    @staticmethod
    def getRewardTier(total):
        try:
            client = MongoManager().client
            db = client["Rewards"]
            reward = db.rewards.find_one({'points': {'$lte': total}}).sort("points", DESCENDING)
        except Exception as e:
            return []
        finally:
            print("Closing the database")
            # close the database
        return reward