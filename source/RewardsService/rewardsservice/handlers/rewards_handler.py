import json
import logging
import math
import re

import tornado.web
from bson.json_util import dumps

from tornado.gen import coroutine

from .root_handler import MongoMixin

log = logging.getLogger(__name__)


class RewardsHandler(MongoMixin):
    order_total = 0

    @staticmethod
    def validate_email(email):
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            raise tornado.web.HTTPError(400, reason='Invalid email')

    def validate_post(self):
        order_total = self.request.decoded_body.get('order_total')
        try:
            self.order_total = float(order_total)
        except ValueError:
            raise tornado.web.HTTPError(400, reason='Order total invalid')

    @coroutine
    @MongoMixin.decode_body
    def post(self):
        email = self.get_query_argument('email')
        self.validate_email(email)
        self.validate_post()
        customer = self.db.rewards.find_one({'email': email})
        if customer:  # existing customer making request, update rewards
            id_ = customer.get('_id')
            reward_points = customer.get('reward_points', 0) + self.order_total
            if reward_points > 1000:
                reward_points = 1000
        else:  # new customer, create
            reward_points = float(self.order_total)
            customer = self.db.rewards.insert_one({'email': email}, {'reward_points': reward_points})
            id_ = customer.inserted_id
        self.db.rewards.update({"_id": id_}, {"$set": {'reward_points': int(reward_points)}})
        customer = self.db.rewards.find_one({'_id': id_})
        self.write(self.response_serializer(*self.get_rewards_for_customer(customer)))

    @coroutine
    def get(self):
        email = self.get_query_argument('email', default=None)
        if email:
            self.validate_email(email)
            customer = self.db.rewards.find_one({'email': email})
            if not customer:
                raise tornado.web.HTTPError(404, reason='Email not found')
            self.write(self.response_serializer(*self.get_rewards_for_customer(customer)))
        else:
            customers = self.db.rewards.find({})  # return all users
            response = []
            for customer in customers:
                if not customer.get('email'):  # this is a tier, not a customer
                    continue
                args = self.get_rewards_for_customer(customer)
                response.append(self.response_serializer(*args))
            self.write({'rewards': response})

    def get_rewards_for_customer(self, customer):
        reward_points = customer.get('reward_points', 0)
        rounded_points = reward_points - (reward_points % 100)
        reward = self.db.rewards.find_one({'points': rounded_points})
        next_reward = self.db.rewards.find_one({'points': rounded_points + 100})
        return customer, reward, next_reward

    @staticmethod
    def response_serializer(customer, current_reward, next_reward):
        next_reward_json = json.loads(dumps(next_reward))
        if next_reward:
            next_reward_json['progress'] = (next_reward.get('points') - customer.get('reward_points', 0)) / 100
        return {
            "customer": json.loads(dumps(customer, sort_keys=True)),
            "current_reward": json.loads(dumps(current_reward, sort_keys=True)),
            "next_reward": next_reward_json
        }
