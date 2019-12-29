import tornado.web

from pymongo import MongoClient


class SingleCustomerHandler(tornado.web.RequestHandler):
    """Returns all customers reward info"""

    def get(self):
        """Accesses and returns list of all customers rewards info"""
        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            customers = list(db.customers.find({}, {"_id": 0}))
            return customers

        except:
            print("Error finding all customers info")
