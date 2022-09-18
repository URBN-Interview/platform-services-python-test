import json
import tornado.web
import re

from tornado.gen import coroutine
from util.db_connection import DBConnection


class CustomerRewardsHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db = DBConnection.get_client()["Rewards"]

    @coroutine
    def prepare(self):
        if self.request.method in ['GET']:
            email = self.get_argument('email', None)
            try:
                self.verifyParams(email)
            except Exception as err:
                self.finishWithError(err)
        if self.request.method in ['POST']:
            try:
                body = json.loads(self.decode_argument(self.request.body))
            except Exception as err:
                self.finishWithError(err)
            email = body.get('email', None)
            order_total = body.get('order_total', None)
            try:
                self.verifyParams(email, order_total)
            except Exception as err:
                self.finishWithError(err)

    @coroutine
    def get(self):
        res = None
        email = self.get_argument('email', None)
        if email is None:
            res = self.fetchAllCustomerRewardsData()
        else:
            res = self.fetchCustomerRewardsData(email)
        self.write(json.dumps(res))

    @coroutine
    def post(self):
        body = json.loads(self.decode_argument(self.request.body))
        email = body.get('email', None)
        order_total = float(body.get('order_total', None))

        customer_rewards = self.fetchCustomerRewardsData(email)
        if customer_rewards is None:
            customer_rewards = {}
        reward_points = order_total + customer_rewards.get('reward_points', 0)

        rewards_tiers = self.fetchRewardsTiers()

        [idx, reward_tier, reward_tier_name] = self.calculate_reward_tier(
            reward_points, rewards_tiers)

        [next_reward_tier, next_reward_tier_name,
            next_reward_tier_progress] = self.calculate_next_reward_tier(idx, reward_points, rewards_tiers)

        updated_customer_rewards = {
            'email': email,
            'reward_points': reward_points,
            'reward_tier': reward_tier,
            'reward_tier_name': reward_tier_name,
            'next_reward_tier': next_reward_tier,
            'next_reward_tier_name': next_reward_tier_name,
            'next_reward_tier_progress': next_reward_tier_progress,
        }

        self.setCustomerRewardsData(email, updated_customer_rewards)

    def verifyParams(self, email=None, order_total=None):
        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if email and not re.fullmatch(regex, email):
            raise Exception("Invalid email")
        if order_total:
            try:
                order_total = float(order_total)
                assert(order_total >= 0)
            except:
                raise Exception("Invalid order total")

    def finishWithError(self, err):
        self.set_status(400)
        self.finish({'message': str(err)})

    def fetchCustomerRewardsData(self, email):
        res = self.db.customerRewards.find_one({"email": email}, {"_id": 0})
        return res

    def setCustomerRewardsData(self, email, updated_customer_rewards):
        customer_rewards = self.fetchCustomerRewardsData(email)
        if customer_rewards is not None:
            self.db.customerRewards.update_one({"email": email},
                                               {"$set": updated_customer_rewards})
        else:
            self.db.customerRewards.insert_one(updated_customer_rewards)

    def fetchAllCustomerRewardsData(self):
        return list(self.db.customerRewards.find({}, {"_id": 0}))

    def fetchRewardsTiers(self):
        return list(self.db.rewards.find({}, {"_id": 0}))

    # Assuming the reward tier system does not change
    # Can tolerate additional tiers on top of 1000 points
    def calculate_reward_tier(self, reward_points, reward_tiers):
        idx = int(reward_points // 100) - 1
        if idx < 0:
            return [-1, None, None]
        if idx >= len(reward_tiers):
            idx = len(reward_tiers) - 1
        reward_tier = reward_tiers[idx]
        return [idx, reward_tier.get('tier', None), reward_tier.get('rewardName', None)]

    def calculate_next_reward_tier(self, idx, reward_points, reward_tiers):
        next_idx = idx+1
        reward_progress = 0
        if next_idx >= len(reward_tiers):
            reward_tier = reward_tiers[-1]
            reward_progress = 100
        else:
            reward_tier = reward_tiers[next_idx]
            reward_progress = reward_points - (reward_tier.get('points') - 100)
        return [reward_tier.get('tier', None), reward_tier.get(
            'rewardName', None), reward_progress]
