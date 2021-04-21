#!/usr/bin/env python3
from pymongo import MongoClient


def main():
    client = MongoClient("mongodb", 27017)
    db = client["Rewards"]
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


if __name__ == "__main__":
    main()