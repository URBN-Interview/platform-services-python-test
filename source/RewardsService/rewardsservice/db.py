# Package to work with Json data
import json
from bson import json_util

#Package for Mongo Db
from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.collection import ReturnDocument

class Database():
    def __init__(self):
        self.client = MongoClient("mongodb", 27017)

# Checks for insertion or updation method to be returned.
    def customer_assertion(self, email_address, order_total):

        # Converting total order into int.
        points_from_order = int(order_total)
        customer = self.get_customer_using_email_address(email_address)
        if customer is None:
            return self.customer_insertion(email_address, points_from_order)

        return self.customer_updation(customer, points_from_order)

# Returns json insertion Record of customer
    def customer_insertion(self, email_address, points):
        db = self.client["Customers"]
        record = self.customer_record_addition(email_address, points)
        db.customers.insert(record)

        # Mongo internal IDs records which are not required
        del record['_id']
        return json.loads(json_util.dumps(record))

# Returns json Updated Record of customer
    def customer_updation(self, customer, points_from_order):
        db = self.client["Customers"]
        updated_customer = self.record_updation_customer(customer, points_from_order)
        db.customers.find_one_and_replace(
            {"email_address": updated_customer.get("email_address")},
            updated_customer)
        return json.loads(json_util.dumps(updated_customer))

# Returns email and reward data of customer
    def customer_record_addition(self, email_address, points):
        return {
            "email_address": email_address,
            **self.points_reward_data(points)
        }

# Returns email and reward data of customer suing total points
    def record_updation_customer(self, customer, points_from_order):
        total_points = customer.get("reward_points") + points_from_order
        return {
            "email_address": customer.get("email_address"),
            **self.points_reward_data(total_points)
        }


    def points_reward_data(self, points):
        current_tier = self.using_points_get_current_tier(points)
        next_tier = self.using_points_get_next_tier(points)

        progress = points / next_tier.get("points") if "points" in next_tier else 0

        return {
            "reward_points": points,
            "reward_tier": current_tier.get("tier", ""),
            "reward_tier_name": current_tier.get("rewardName", ""),
            "next_reward_tier": next_tier.get("tier", ""),
            "next_reward_tier_name": next_tier.get("rewardName", ""),
            "next_reward_tier_progress": progress
        }


    def using_points_get_current_tier(self, points):
        db = self.client["Rewards"]
        tier_list = list(db.rewards.find({"points": {"$lte": points}}).sort('points', DESCENDING))
        if len(tier_list) == 0:
            return {}
        return json.loads(json_util.dumps(tier_list[0]))


    def using_points_get_next_tier(self, points):
        db = self.client["Rewards"]
        tier_list = list(db.rewards.find({"points": {"$gt": points}}).sort('points', ASCENDING))
        if len(tier_list) == 0:
            return {}
        return json.loads(json_util.dumps(tier_list[0]))


    def get_customer_using_email_address(self, email_address):
        db = self.client["Customers"]
        customers = list(db.customers.find({'email_address': email_address}))
        if len(customers) == 0:
            return None
        customer = customers[0]
        del customer['_id'] # don't return Mongo internal IDs
        return json.loads(json_util.dumps(customer))


    def get_every_customers(self):
        db = self.client["Customers"]
        customers = list(db.customers.find({}))
        for customer in customers:
             # Mongo internal IDs records which are not required
             del customer['_id']
        return json.loads(json_util.dumps(customers))