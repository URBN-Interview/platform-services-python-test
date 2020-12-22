import re
import tornado.web
from pymongo import MongoClient

email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def validate_email(email):
    if re.search(email_regex, email):
        return True
    else:
        return False


def validate_order_total(order_total):
    if re.match(r'^-?\d+(?:\.\d+)?$', order_total) is not None:
        return True
    else:
        return False


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        client = MongoClient("mongodb", 27017)
        self.db = client["Rewards"]
