import json
import tornado.web
from tornado.gen import coroutine
import re


class CustomerRewardsHandler(tornado.web.RequestHandler):

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

    def get_customer_by_email(self, email):
        customer = self.settings["db"].customerRewards.find_one(
            {"email": email}, {"_id": 0})
        return customer

    def get_all_customer_reward_data(self):
        customer = list(
            self.settings["db"].customerRewards.find({}, {"_id": 0}))
        return customer
