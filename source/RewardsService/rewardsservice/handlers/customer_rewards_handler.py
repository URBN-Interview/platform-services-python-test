import json
import tornado.web
import logging

from pymongo import MongoClient
from tornado.gen import coroutine
from handlers.base import BaseHandler
from util.error_throw import ErrorThrow
from util.jsonencoder import JSONEncoder
from http import HTTPStatus

class CustomerRewardsHandler(BaseHandler):

    def data_received(self, chunk=None):
        if self.request.body:
            return tornado.escape.json_decode(self.request.body)

    # to calculate current and next reward stats
    def calculatecustomerrewards(self, dbu, customers_total_points):
        cust_reward = self.data_received()
        cust_reward['points'] = customers_total_points
        del cust_reward['orderTotal'];

        max_reward_tiers = dbu.rewards.find().sort("points", -1).limit(1)
        if max_reward_tiers.count() > 0:
            max_reward_tier = max_reward_tiers.next()
            if (max_reward_tier) is not None:
                max_reward_points_allowed = max_reward_tier.get('points')

        qualified_rewards_tier_points = int(customers_total_points/100)*100
        print(qualified_rewards_tier_points)
        qualified_rewards_tiers = dbu.rewards.find({"points": { "$lte": qualified_rewards_tier_points }}).sort("points", -1).limit(1)
        #reward_tier = dbu.rewards.find_one({'points': qualified_rewards_tier_points})
        if qualified_rewards_tiers.count() > 0:
            qualified_rewards_tier = qualified_rewards_tiers.next()
            if (qualified_rewards_tier) is not None:
                cust_reward['current_tier'] = qualified_rewards_tier.get('tier')
                cust_reward['current_rewardName'] = qualified_rewards_tier.get('rewardName')

        next_reward_tiers = dbu.rewards.find({"points": { "$gt": qualified_rewards_tier_points }}).sort("points", +1).limit(1)
        if next_reward_tiers.count() > 0:
            next_reward_tier = next_reward_tiers.next()
            if (next_reward_tier) is not None:
                cust_reward['next_tier'] = next_reward_tier.get('tier')
                cust_reward['next_rewardName'] = next_reward_tier.get('rewardName')
                need_more_to_get_next = (next_reward_tier.get('points') - customers_total_points)*100/(next_reward_tier.get('points') - qualified_rewards_tier_points)
                cust_reward['need_more_to_get_next'] = int(need_more_to_get_next)
        else:
            cust_reward['need_more_to_get_next'] = 0
            if (qualified_rewards_tier) is not None:
                cust_reward['next_tier'] = qualified_rewards_tier.get('tier')
                cust_reward['next_rewardName'] = qualified_rewards_tier.get('rewardName')
        return cust_reward

    # to update current and next reward stats in customer account
    def updatecustomerrewards(self, email, customers_total_points):
        client = MongoClient("mongodb", 27017)
        dbu = client["Rewards"]
        cust_reward_obj = self.calculatecustomerrewards(dbu, customers_total_points)
        try:
            dbu.customerrewards.update_one({"email": email}, {"$set": cust_reward_obj})
        except Exception as ex:
                logging.getLogger().error(ex)
                raise ErrorThrow(status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
                                 reason=str(ex))
        else:
            updated_rec = dbu.customerrewards.find_one({'email': email})
            if (updated_rec) is not None:
                #self.set_status(200)
                #self.write(JSONEncoder().encode(updated_rec))
                self.write_response(status_code=HTTPStatus.OK.value,
                                    result=JSONEncoder().encode(updated_rec))

    # returning customer rewards data
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer_email = self.get_argument('email', True)
        
        if customer_email != True:
            customer_rewards_data = list(db.customerrewards.find({'email': customer_email}, {"_id": 0}))
        else:
            customer_rewards_data = list(db.customerrewards.find({}, {"_id": 0}))
        if not customer_rewards_data:
            self.write_response(status_code=HTTPStatus.NO_CONTENT.value,
                                    result=customer_rewards_data)
        else:
            self.write_response(status_code=HTTPStatus.OK.value,
                                    result=customer_rewards_data)

    # creating or updating customer rewards data
    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        dbp = client["Rewards"]
        #dbp.customerrewards.remove()
        customer_email = self.data_received().get('email')
        order_value = self.data_received().get('orderTotal')
        customers_earned_points = int(order_value)
        if(customers_earned_points) is None:
            customers_earned_points = 0
        customer_exists = dbp.customerrewards.find_one({'email': customer_email})
        if (customer_exists) is not None:
            customers_existing_points = customer_exists.get('points')
            if(customers_existing_points) is not None:
                customers_total_points = customers_existing_points + customers_earned_points
            else:
                customers_total_points = customers_earned_points
            self.updatecustomerrewards(customer_email, customers_total_points)
        else:
            try:
                record_to_insert = self.calculatecustomerrewards(dbp, customers_earned_points)
                inserted_rec = dbp.customerrewards.insert_one(record_to_insert)
            except Exception as ex:
                    logging.getLogger().error(ex)
                    raise ErrorThrow(status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
                                    reason=str(ex))
            else:
                created_rec = dbp.customerrewards.find_one({'_id': inserted_rec.inserted_id})
                #self.set_status(201)
                #self.write(JSONEncoder().encode(created_rec))
                self.write_response(status_code=HTTPStatus.CREATED.value,
                                    result=JSONEncoder().encode(created_rec))
