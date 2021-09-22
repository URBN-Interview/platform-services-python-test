import re

from pymongo import MongoClient


def get_mongo_connection():
    client = MongoClient("mongodb", 27017)
    db = client["Rewards"]
    return db


def get_rewards_configs(db):
    rewards = list(db.rewards.find({}, {"_id": 0}))
    rewards = sorted(rewards, key=lambda x: x.get("points"))
    return rewards


def get_customer_by_email(db, email):
    customers = list(db.customers.find({"email":email}, {"_id": 0}))
    return customers


def create_customer(db, data):
    email = data.get("email")
    customer = get_customers_data(db, email)
    if customer:
        return update_customer(db, data) 
    customer = {}
    customer["email"] = data.get("email")
    customer["order_total"] = 0
    customer["reward_points"] = 0
    customer["reward_tier"] = ""
    customer["reward_tier_name"] = ""
    customer["next_reward_tier"] = ""
    customer["next_reward_tier_name"] = ""
    customer["next_reward_tier_progress"] = ""
    order_total = float(data.get("order_total"))
    customer = add_calculations(db, customer, order_total)
    res = db.customers.insert(customer)
    return customer


def update_customer(db, data):
    email = data.get("email")
    customer = get_customers_data(db, email)
    if not customer:
        raise Exception(f"Customer Not Found with Given Email {email}")
    order_total = float(data.get("order_total"))
    customer = add_calculations(db, customer, order_total)
    email = data.get("email")
    db.customers.update({"email": email}, customer)
    customer = get_customers_data(db, email)
    return customer


def get_customers_data(db, email):
    customers = list(db.customers.find({"email":email}, {"_id": False}))
    return customers[0] if customers else None


def get_customers(db):
    customers = list(db.customers.find({}, {"_id": False}))
    return customers


def add_calculations(db, customer, order_total):
    rewards = get_rewards_configs(db)
    customer["order_total"] = round(customer.get("order_total", 0) + float(order_total), 2)
    reward_points = customer.get("reward_points", 0) + int(float(order_total))
    customer["reward_points"] = reward_points
    
    previous_reward = rewards[0]
    if reward_points < previous_reward["points"]:
        customer["reward_tier"] = ""
        customer["reward_tier_name"] = ""
        customer["next_reward_tier"] = previous_reward["tier"]
        customer["next_reward_tier_name"] = previous_reward["rewardName"]
        customer["next_reward_tier_progress"] = round(((previous_reward["points"] - reward_points) / previous_reward["points"])*100, 2)
        return customer
    
    last_reward = rewards[-1]
    if reward_points > last_reward["points"]:
        customer["reward_tier"] = last_reward["tier"]
        customer["reward_tier_name"] = last_reward["rewardName"]
        customer["next_reward_tier"] = "NA"
        customer["next_reward_tier_name"] = "NA"
        customer["next_reward_tier_progress"] = "NA"
        return customer
    
    for item in rewards[1:]:
        if not (previous_reward["points"] <= reward_points  < item["points"]):
            previous_reward = item
            continue
        customer["reward_tier"] = previous_reward["tier"]
        customer["reward_tier_name"] = previous_reward["rewardName"]
        customer["next_reward_tier"] = item["tier"]
        customer["next_reward_tier_name"] = item["rewardName"]
        progress = 100 - round(((item["points"] - reward_points) / (item["points"] - previous_reward["points"]) )*100, 2)
        customer["next_reward_tier_progress"] = 0.0 if progress >= 100 else progress
        return customer
    return customer
