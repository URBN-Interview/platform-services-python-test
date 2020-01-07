import tornado.web
import json

from pymongo import MongoClient
from tornado.gen import coroutine


class AllCustomersHandler(tornado.web.RequestHandler):
    """Returns all customers reward info"""

    @coroutine
    def get(self):
        """Accesses and returns list of all customers rewards info"""
        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            customers = db["customers"]
            customers = list(customers.find({}, {"_id": 0}))
            self.write(json.dumps(customers))
        except ValueError:
            self.write("A value error occurred")
        except TypeError:
            self.write("A type error has occurred")
        except RuntimeError:
            self.write("Error finding all customers info")
