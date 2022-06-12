import json
import tornado.web
from tornado.gen import coroutine
import re
from pymongo import DESCENDING


class CustomerRewardsHandler(tornado.web.RequestHandler):
    @coroutine
    def post(self):
        email = self.get_email(True)
        points = self.get_total()
        customer = self.get_customer_by_email(email, False)
        if customer:
            currPoints = customer["rewardPoints"] if customer else 0
            points += currPoints
        reward_data = self.get_reward_level(points)
        formatted_object = self.format_customer_upsert_object(
            reward_data, email, points)
        self.replace_customer_data(email, formatted_object)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(formatted_object))

    @coroutine
    def get(self):
        email = self.get_email(False)
        if email:
            customers = self.get_customer_by_email(email)
        else:
            customers = self.get_all_customer_reward_data()
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(customers))

    def get_email(self, req):
        email = self.get_argument('email', None, True)
        if req and not email:
            raise ValueError('Email is required')
        regex = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
        if(req and not re.fullmatch(regex, email)):
            raise ValueError(email + ' is not a valid email')
        return email

    def get_total(self):
        total = self.get_argument('total', None, True)
        regchecktotal = re.match(
            '(?=.*?\d)?(([1-9]\d{0,2}(,\d{3})*)|\d+)?(\.\d{1,2})?$', total)
        if not regchecktotal:
            raise ValueError(
                'Total can only be a float number with digits only and up to 2 decimal points.')
        else:
            actualtotal = int(float(regchecktotal.groups()[0]))
        if actualtotal < 0:
            raise ValueError('Total must be greater than 0')
        return actualtotal

    def get_customer_by_email(self, email, req=True):
        customer = self.settings["db"].customerRewards.find_one(
            {"email": email}, {"_id": 0})
        
        return customer

    def get_all_customer_reward_data(self):
        customer = list(
            self.settings["db"].customerRewards.find({}, {"_id": 0}))
        return customer

    def replace_customer_data(self, email, customer_object):
        self.settings["db"].customerRewards.replace_one(
            {"email": email}, customer_object, upsert=True)
        return

    def get_reward_level(self, points):
        floor_points = float(points / 100) 
        floor_points *= 100
        if floor_points >= 1000:
            return list([{}, self.settings["db"].rewards.find_one({'points': 1000}, {"_id": 0})])
        if floor_points < 100:
            return list([self.settings["db"].rewards.find_one({'points': 100}, {"_id": 0}), {}])
        return list(self.settings["db"].rewards.find({'points': {
            '$in': [floor_points, floor_points+100]}}, sort=[('points', DESCENDING)]))

    def format_customer_upsert_object(self, reward_data, email, points):
        formatted_customer_object = {
            "email": email,
            "rewardPoints": points,
            "rewardTier": reward_data[1].get("tier") if reward_data[1] else '',
            "rewardTierName": reward_data[1].get("rewardName") if reward_data[1] else '',
            "nextRewardTier": reward_data[0].get("tier") if reward_data[0] else '',
            "nextRewardTierName": reward_data[0].get("rewardName") if reward_data[0] else '',
            "nextRewardTierProgress": points / reward_data[0].get("points") if reward_data[0].get("points") else "",
        }
        return formatted_customer_object
