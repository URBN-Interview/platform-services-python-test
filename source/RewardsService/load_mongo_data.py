#!/usr/bin/env python
from pymongo import MongoClient


def generate_rewards(db):
    print("Removing and reloading customers in mongo")
    db.customers.remove()
    db.customers.insert(
        {"emailAddress": "christian.lomboy@icloud.com", "points": 100, "tier": "A", "rewardName": "5% off purchase",
         "nextTier": "B", "nextRewardName": "10% off purchase", "nextTierProgress": 0.5})
    db.customers.insert(
        {"emailAddress": "john.appleseed@icloud.com", "points": 300, "tier": "C", "rewardName": "15% off purchase",
         "nextTier": "D", "nextRewardName": "20% off purchase", "nextTierProgress": 0.7})
    print("Customers loaded in mongo")


def generate_customers(db):
    print("Removing and reloading rewards in mongo")
    db.rewards.remove()
    db.rewards.insert({"points": 100, "rewardName": "5% off purchase", "tier": "A"})
    db.rewards.insert({"points": 200, "rewardName": "10% off purchase", "tier": "B"})
    db.rewards.insert({"points": 300, "rewardName": "15% off purchase", "tier": "C"})
    db.rewards.insert({"points": 400, "rewardName": "20% off purchase", "tier": "D"})
    db.rewards.insert({"points": 500, "rewardName": "25% off purchase", "tier": "E"})
    db.rewards.insert({"points": 600, "rewardName": "30% off purchase", "tier": "F"})
    db.rewards.insert({"points": 700, "rewardName": "35% off purchase", "tier": "G"})
    db.rewards.insert({"points": 800, "rewardName": "40% off purchase", "tier": "H"})
    db.rewards.insert({"points": 900, "rewardName": "45% off purchase", "tier": "I"})
    db.rewards.insert({"points": 1000, "rewardName": "50% off purchase", "tier": "J"})
    print("Rewards loaded in mongo")


def main():
    client = MongoClient("mongodb", 27017)
    db = client["Rewards"]

    generate_rewards(db)
    generate_customers(db)


if __name__ == "__main__":
    main()
