import json
import tornado.web
from bson import json_util
from pymongo import MongoClient
from tornado.gen import coroutine
from tornado import escape
import uuid
from math import floor
from bson.json_util import dumps
from bson.json_util import loads
from rewardsservice.customer.Customer import Customer
from .reward_calculators import RewardCalculators
from rewardsservice.error_handling.error_handling import EmailErrorHandler



class CustomerOrderDataHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self) -> str:

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer_order_data_collection = db["customerOrderData"]

        result = tornado.escape.json_decode(self.request.body)
        
        customer = Customer()

        validate_email = EmailErrorHandler()

        validation = validate_email.validate_email_address(result["Email Address"])
        if isinstance(validation, list):
            self.write(validation[0])
        else:
            customer.email_address = result["Email Address"]


            order_total = float(result["Order Total"])
            reward_calculators = RewardCalculators()

            customer.reward_points = reward_calculators.calculateRewardPoints(order_total, customer.reward_points)
            customer.reward_tier = reward_calculators.calculateRewardTier(customer.reward_points)
            customer.reward_tier_name = reward_calculators.generateRewardTierName(customer.reward_tier)
            customer.next_reward_tier = reward_calculators.calculateNextTierAndNextTierName(customer.reward_tier)[0]
            customer.next_reward_tier_name = reward_calculators.calculateNextTierAndNextTierName(customer.reward_tier)[1]
            customer.next_reward_tier_progress = reward_calculators.calculateNextTierProgress(customer.reward_points)


            customer_rewards_data = {
                "_id": uuid.uuid4(),
                "Email Address": result["Email Address"],
                "Reward Points": customer.reward_points,
                "Reward Tier": customer.reward_tier,
                "Reward Tier Name": customer.reward_tier_name,
                "Next Reward Tier": customer.next_reward_tier,
                "Next Reward Tier Name": customer.next_reward_tier_name,
                "Next Reward Tier Progress":customer.next_reward_tier_progress
                                        }

            customer_order_data_collection.insert_one(customer_rewards_data)
            self.write("Customer Order Data Stored Successfully!")