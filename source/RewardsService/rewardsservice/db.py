import json
from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.collection import ReturnDocument
from bson import json_util

class Database():
    def __init__(self):
        self.client = MongoClient("mongodb", 27017)

    def upsert_customer(self, email_address, order_total):
        points_from_order = int(order_total) # rounds down

        customer = self.get_customer_by_email_address(email_address)
        if customer is None:
            return self.insert_customer(email_address, points_from_order)

        return self.update_customer(customer, points_from_order)


    def insert_customer(self, email_address, points):
        db = self.client["Customers"]
        record = self.new_customer_record(email_address, points)
        db.customers.insert(record)
        del record['_id'] # don't return Mongo internal IDs
        return json.loads(json_util.dumps(record))


    def update_customer(self, customer, points_from_order):
        db = self.client["Customers"]
        updated_customer = self.updated_customer_record(customer, points_from_order)
        db.customers.find_one_and_replace(
            {"email_address": updated_customer.get("email_address")},
            updated_customer)
        return json.loads(json_util.dumps(updated_customer))


    def new_customer_record(self, email_address, points):
        return {
            "email_address": email_address,
            **self.new_reward_data_for_points(points)
        }


    def updated_customer_record(self, customer, points_from_order):
        total_points = customer.get("reward_points") + points_from_order
        return {
            "email_address": customer.get("email_address"),
            **self.new_reward_data_for_points(total_points)
        }


    def new_reward_data_for_points(self, points):
        current_tier = self.get_current_tier_by_points(points)
        next_tier = self.get_next_tier_by_points(points)

        return {
            "reward_points": points,
            "reward_tier": current_tier.get("tier", ""),
            "reward_tier_name": current_tier.get("rewardName", ""),
            "next_reward_tier": next_tier.get("points", ""),
            "next_reward_tier_name": next_tier.get("tier", ""),
            "next_reward_tier_progress": next_tier.get("rewardName", "")
        }


    def get_current_tier_by_points(self, points):
        db = self.client["Rewards"]
        tier_list = list(db.rewards.find({"points": {"$lte": points}}).sort('points', DESCENDING))
        if len(tier_list) == 0:
            return {}
        return json.loads(json_util.dumps(tier_list[0]))


    def get_next_tier_by_points(self, points):
        db = self.client["Rewards"]
        tier_list = list(db.rewards.find({"points": {"$gt": points}}).sort('points', ASCENDING))
        if len(tier_list) == 0:
            return {}
        return json.loads(json_util.dumps(tier_list[0]))


    def get_customer_by_email_address(self, email_address):
        db = self.client["Customers"]
        customers_list = list(db.customers.find({'email_address': email_address}))
        if len(customers_list) == 0:
            return None
        return json.loads(json_util.dumps(customers_list[0]))