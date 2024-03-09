#!/usr/bin/env python
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Define the rewards data to be inserted into the MongoDB collection
REWARDS_DATA = [
    {"points": 100, "rewardName": "5% off purchase", "tier": "A"},
    {"points": 200, "rewardName": "10% off purchase", "tier": "B"},
    {"points": 300, "rewardName": "15% off purchase", "tier": "C"},
    {"points": 400, "rewardName": "20% off purchase", "tier": "D"},
    {"points": 500, "rewardName": "25% off purchase", "tier": "E"},
    {"points": 600, "rewardName": "30% off purchase", "tier": "F"},
    {"points": 700, "rewardName": "35% off purchase", "tier": "G"},
    {"points": 800, "rewardName": "40% off purchase", "tier": "H"},
    {"points": 900, "rewardName": "45% off purchase", "tier": "I"},
    {"points": 1000, "rewardName": "50% off purchase", "tier": "J"}
]


def connect_to_mongodb():
    """
    Connect to MongoDB server.

    Returns:
        MongoClient or None: A MongoClient object if connection successful, otherwise None.
    """
    try:
        client = MongoClient("mongodb://localhost:27017")
        return client
    except ConnectionFailure:
        print("Failed to connect to MongoDB")
        return None


def load_rewards(db):
    """
    Load rewards data into MongoDB collection.

    Args:
        db (Database): The MongoDB database object.
    """
    try:
        # Remove existing rewards data
        db.rewards.delete_many({})
        # Insert new rewards data in bulk
        db.rewards.insert_many(REWARDS_DATA)
        print("Rewards loaded in MongoDB")
    except Exception as e:
        print(f"Error loading rewards: {e}")


def main():
    """Main function to manage rewards data in MongoDB."""
    # Connect to MongoDB
    client = connect_to_mongodb()
    if client:
        db = client["Rewards"]
        print("Removing and reloading rewards in MongoDB")
        # Load rewards data
        load_rewards(db)
        # Close MongoDB connection
        client.close()


if __name__ == "__main__":
    main()

