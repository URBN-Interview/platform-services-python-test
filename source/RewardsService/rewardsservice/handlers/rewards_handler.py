import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
import re


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))


class ManageCustomer(tornado.web.RequestHandler):

    def get(self):
        self.write("Api is post only.")

    def post(self):
        client = MongoClient("mongodb", 27017)
        email_address = self.get_argument("email_address", None)
        order_total = self.get_argument("order_total", None)

        # Check if email_address or order_total were not in the post data
        if not email_address or not order_total:
            return(self.write("Error: Missing data"))

        # Check if email address is valid
        if not check_email(email_address):
            return(self.write("Error: Invalid Email Address"))

        # Check if order_total is valid
        point_total = check_order_total(order_total)
        if not point_total:
            return(self.write("Error: Invalid Order Total"))

        # Search DB for customer, add or update
        db = client["Customers"]
        customer = db.customers.find_one(
            {"email_address": email_address},
            {"point_total": 1})

        if customer:
            points = customer["point_total"]
            db.customers.update_one(
                {'_id': customer["_id"]},
                {'$set': {"point_total": points + point_total}},
                upsert=False)
        else:
            db.customers.insert({"email_address": email_address, "point_total": point_total})


def check_email(email_address):
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if(re.search(regex, email_address)):
        return(True)

    return(False)


def check_order_total(order_total):
    order_total = order_total.replace("$", "")
    if order_total.isnumeric():
        return(int(order_total))
    return(False)
