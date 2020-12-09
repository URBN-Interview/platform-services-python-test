#!/usr/bin/env python
import pymongo
from pymongo import MongoClient


def main():
    client = MongoClient("mongodb", 27017)
    db = client["Rewards"]

    print("Removing and reloading rewards in mongo")
    db.rewards.delete_many({})
    db.rewards.insert_one({"tier": "A", "rewardName": "5% off purchase", "points": 100}),
    db.rewards.insert_one({"tier": "B", "rewardName": "10% off purchase", "points": 200}),
    db.rewards.insert_one({"tier": "C", "rewardName": "15% off purchase", "points": 300}),
    db.rewards.insert_one({"tier": "D", "rewardName": "20% off purchase", "points": 400}),
    db.rewards.insert_one({"tier": "E", "rewardName": "25% off purchase", "points": 500}),
    db.rewards.insert_one({"tier": "F", "rewardName": "30% off purchase", "points": 600}),
    db.rewards.insert_one({"tier": "G", "rewardName": "35% off purchase", "points": 700}),
    db.rewards.insert_one({"tier": "H", "rewardName": "40% off purchase", "points": 800}),
    db.rewards.insert_one({"tier": "I", "rewardName": "45% off purchase", "points": 900}),
    db.rewards.insert_one({"tier": "J", "rewardName": "50% off purchase", "points": 1000})
    print("Rewards loaded in mongo")


def updateCustomerData(email, points):
    client = MongoClient("mongodb", 27017)
    db = client["Rewards"]

    customer = db.customer_data.find_one({"email": email})

    # If customer exists, update their rewards and tiers
    if customer is not None and customer["points"] < 1000:
        newPoints = customer["points"] + points

        roundedPoints = newPoints - (newPoints % 100)

        if roundedPoints >= 1000:
            db.customer_data.update_one({"email": email}, {"$set": {"points": roundedPoints,
                                                                    "tier": "J",
                                                                    "rewardName": "50% off purchase",
                                                                    "nextTier": "None",
                                                                    "nextRewardName": "None",
                                                                    "nextTierProgress": 0}})
            return

        current_query = {"points": {"$eq": roundedPoints}}
        next_query = {"points": {"$eq": roundedPoints+100}}

        current_tier = db.rewards.find_one(current_query)

        next_tier = db.rewards.find_one(next_query)

        db.customer_data.update_one({"email": email}, {"$set": {"points": newPoints,
                                                                "tier": current_tier["tier"],
                                                                "rewardName": current_tier["rewardName"],
                                                                "nextTier": next_tier["tier"],
                                                                "nextRewardName": next_tier["rewardName"],
                                                                "nextTierProgress": next_tier["points"]}})

        return

    # Do nothing if the customer's rewards are maxed out
    elif customer is not None and customer["points"] >= 1000:
        return

    roundedPoints = points - (points % 100)

    if roundedPoints >= 1000:
        db.customer_data.insert_one({"email": email, "points": roundedPoints,
                                    "tier": "J", "rewardName": "50% off purchase",
                                    "nextTier": "None", "nextRewardName": "None",
                                    "nextTierProgress": 0})
        return

    # Customer doesn't exist in database, add them to start rewards
    current_query = {"points": {"$eq": roundedPoints}}
    next_query = {"points": {"$eq": roundedPoints+100}}

    current_tier = db.rewards.find_one(current_query)
    next_tier = db.rewards.find_one(next_query)

    db.customer_data.insert_one({"email": email, "points": points,
                                 "tier": current_tier["tier"], "rewardName": current_tier["rewardName"],
                                 "nextTier": next_tier["tier"], "nextRewardName": next_tier["rewardName"],
                                 "nextTierProgress": next_tier["points"]})

    #db.customer_data.delete_many({})

def returnRewards(email):
    client = MongoClient("mongodb", 27017)
    db = client["Rewards"]

    customer = db.customer_data.find_one({"email": email})

    if customer is not None:
        return {"points": customer["points"], "tier": customer["tier"], "rewardName": customer["rewardName"],
                                 "nextTier": customer["tier"], "nextRewardName": customer["rewardName"],
                                 "nextTierProgress": customer["points"]}
    else:
        return "Not a rewards member."

if __name__ == "__main__":
    main()
