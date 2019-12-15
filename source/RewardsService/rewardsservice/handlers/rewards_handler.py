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
            return(self.write(json.dumps({'order_error': "Missing data"})))

        # Check if email address is valid
        if not check_email(email_address):
            return(self.write(json.dumps({'order_error': "Invalid Email Address"})))

        # Check if order_total is valid
        point_total = check_order_total(order_total)
        if not point_total:
            return(self.write(json.dumps({'order_error': "Invalid Order Total"})))

        # Search DB for customer, add or update
        db = client["Customers"]
        customer = db.customers.find_one(
            {"email_address": email_address},
            {"reward_points": 1})

        if customer:
            points = customer["reward_points"] + point_total
            reward_info = get_reward_info(points)
            db.customers.update_one(
                {'_id': customer["_id"]},
                {'$set': reward_info},
                upsert=False)
            reward_info.update({'email_address': email_address})

        else:
            reward_info = get_reward_info(point_total)
            reward_info.update({'email_address': email_address})
            db.customers.insert(reward_info)

        self.write(json.dumps({'order_success': "Order added successfully!"}))


class GetCustomer(tornado.web.RequestHandler):

    def get(self, email_address):
        client = MongoClient("mongodb", 27017)
        dbc = client["Customers"]

        customer = dbc.customers.find_one(
            {'email_address': email_address},
            {"_id": 0})

        self.write(json.dumps(customer))


class GetAllCustomers(tornado.web.RequestHandler):

    def get(self):
        client = MongoClient("mongodb", 27017)
        dbc = client["Customers"]
        customer = list(dbc.customers.find({}, {"_id": 0}))
        self.write(json.dumps(customer))


def get_reward_info(points):

    current_points = (points // 100) * 100
    current_points = 1000 if current_points >= 1000 else current_points
    next_points = 1000 if current_points >= 1000 else current_points + 100

    client = MongoClient("mongodb", 27017)
    dbr = client["Rewards"]
    current_reward = dbr.rewards.find_one(
        {"points": current_points},
        {"_id": 0, "points": 0})
    next_reward = dbr.rewards.find_one(
        {"points": next_points},
        {"_id": 0, "points": 0})

    if not current_reward:
        current_reward = {"tier": "0", "rewardName": "0% off purchase"}

    if current_points == 1000:
        next_progress = 0
    else:
        next_progress = 1 - ((points / 100) - (current_points / 100))

    return({
        "reward_points": points,
        "reward_tier": current_reward['tier'],
        "reward_tier_name": current_reward['rewardName'],
        "next_reward_tier": next_reward['tier'],
        "next_reward_tier_name": next_reward['rewardName'],
        "next_reward_tier_progress": next_progress})


def check_email(email_address):
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if(re.search(regex, email_address)):
        return(True)

    return(False)


def check_order_total(order_total):
    order_total = order_total.replace("$", "")
    try:
        return(int(float(order_total)))
    except ValueError:
        return(False)
