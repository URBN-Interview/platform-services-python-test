import json
import tornado.web
import tornado.escape

from pymongo import MongoClient
from tornado.gen import coroutine

import logging


def calculateUpdatedTiers(rewardPoints, rewards):
    '''
    Calculates  user's current and next reward tears
    Takes in:
      - rewardPoints: int (User's current reward points)
      - rewards: list (all reward tiers)

    Returns the current and next tier
    '''
    if rewardPoints < rewards[0]["points"]:
        return {"tier": "", "rewardName": "", "points": 0}, rewards[0]
    for i in range(1, len(rewards)):
        if rewardPoints < rewards[i]["points"]:
            return rewards[i-1], rewards[i]
    return rewards[-1], rewards[-1]


class OrderHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        '''
        Updates user's rewards information
        Takes in:
          - email: string (User's email)
          - orderTotal: double (Total order)

        '''
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        try:
            # Sort the list to make sure the rewards are in order based on points
            rewards = sorted(list(db.rewards.find({}, {"_id": 0})),
                             key=lambda reward: reward["points"])
        except:
            raise tornado.web.HTTPError(
                status_code=500, log_message="Database connection failed")

        try:
            # Extract email and order total from the request
            requestBody = tornado.escape.json_decode(self.request.body)
            email = requestBody["email"]
            orderTotal = requestBody["orderTotal"]

            customer = db.customers.find_one({"email": email})
            if customer == None:
                customer = {"email": email, "rewardPoints": 0, "rewardTier": "", "rewardTierName": "",
                            "nextRewardTier": "A", "nextRewardTierName": "5% off purchase", "nextRewardTierProgress": 0}
                _id = db.customers.insert_one(customer).inserted_id
                customer["_id"] = _id

            # If the user is already at top tier, no need to do calculations
            if customer["rewardTier"] == rewards[-1]["tier"]:
                self.finish(json.dumps({"nextRewardTierName": customer["nextRewardTierName"],
                                        "nextRewardTier": customer["nextRewardTier"],
                                        "nextRewardTierProgress": 1,
                                        "rewardTierName": customer["rewardTierName"],
                                        "email": email,
                                        "rewardPoints": customer["rewardPoints"],
                                        "rewardTier": customer["rewardTier"]}))
                return

            currentRewardPoints = customer["rewardPoints"]
            updatedRewardPoints = currentRewardPoints + int(orderTotal)

            (currentTier, nextTier) = calculateUpdatedTiers(
                updatedRewardPoints, rewards)

            # Creating a new dictionary for the updated fields to only update what's needed
            updatedFields = {}
            updatedFields["rewardPoints"] = updatedRewardPoints
            updatedFields["rewardTier"] = currentTier["tier"]
            updatedFields["rewardTierName"] = currentTier["rewardName"]
            updatedFields["nextRewardTier"] = nextTier["tier"]
            updatedFields["nextRewardTierName"] = nextTier["rewardName"]

            # Top tier
            if currentTier["points"] == nextTier["points"]:
                updatedFields["nextRewardTierProgress"] = 1
            else:
                # Calculating the percentage as the progress between current tier and next tier
                updatedFields["nextRewardTierProgress"] = (updatedRewardPoints-currentTier["points"]) / \
                    (nextTier["points"] - currentTier["points"])

            if updatedFields["rewardPoints"] >= rewards[-1]["points"]:
                updatedFields["rewardPoints"] = rewards[-1]["points"]

            # Update the customer in the database
            db.customers.update_one({"_id": customer["_id"]}, {
                                    "$set": updatedFields})

            # Add the email to the response dictionary
            updatedFields["email"] = email
            # Returning the updated customer information back so that it can be updated in the frontend without fetching again
            self.finish(json.dumps(updatedFields))
            return

        except KeyError as e:
            logging.debug(e)
            raise tornado.web.HTTPError(
                status_code=422, log_message="Email and order total are required")
        except Exception as e:
            raise tornado.web.HTTPError(
                status_code=400, log_message="Something went wrong")

        raise tornado.web.HTTPError(
            status_code=400, log_message="Something went wrong")
