import json
import tornado.web
import math

from pymongo import MongoClient
from tornado.gen import coroutine
from tornado.web import HTTPError, MissingArgumentError

"""
Endpoint 1:
    * Accept a customer's order data: email address (ex. "customer01@gmail.com") and order total (ex. 100.80).
    Calculate and store the following customer rewards data into MongoDB. 
    For each dollar a customer spends, the customer will earn 1 reward point. 
    For example, an order of $100.80 earns 100 points. 
    Once a customer has reached the top rewards tier, there are no more rewards the customer can earn.
        1. Email Address: the customer's email address (ex. "customer01@gmail.com")
        2. Reward Points: the customer's rewards points (ex. 100)
        3. Reward Tier: the rewards tier the customer has reached (ex. "A")
        4. Reward Tier Name: the name of the rewards tier (ex. "5% off purchase")
        5. Next Reward Tier: the next rewards tier the customer can reach (ex. "B")
        6. Next Reward Tier Name: the name of next rewards tier (ex. "10% off purchase")
        7. Next Reward Tier Progress: the percentage the customer is away from reaching the next rewards tier (ex. 0.5)

customer data format:

{
    email: str,
    points: int,
    tier: str,
    tierName: str,
    nextTier: str,
    nextTierName: str,
    nextTierProgress: float
}
"""


class AddOrderHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        # get arguments
        try:
            email = self.get_argument('email')
            total = self.get_argument('order-total', 0)
        except MissingArgumentError as e:
            self.write_error(e.status_code)
            return

        # fetch both the rewards and customers collections
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        current_customers = list(db.customers.find({}, {"_id": 0}))

        # calculate points earned (1 point / full dollar spent) and see if a customer with the given email exists
        points_earned = math.floor(float(total))
        existing_customer = None
        for customer in current_customers:
            if email in customer.values():
                existing_customer = customer

        if existing_customer is not None:
            # add the points spent to the current customer's total
            new_total = existing_customer['points'] + points_earned

            # we can find the proper index of the current reward tier because they are stored in the db in order
            # example: if a user has 110 points, they would be at index 0 (110 / 100) => (1) - 0 = 0
            rewards_index = int((new_total / 100)) - 1
            progress_amount = (new_total % 100.) / 100.
            curr_tier = rewards[rewards_index if rewards_index < 9 else 9]
            next_tier = rewards[rewards_index + 1 if rewards_index < 9 else 9]

            # the email_query is used to find the object to update with the new_values
            email_query = {
                "email": email
            }
            new_values = {
                "$set": {
                    "points": new_total,
                    "tier": curr_tier['tier'],
                    "tierName": curr_tier['rewardName'],
                    "nextTier": next_tier['tier'],
                    "nextTierName": next_tier['rewardName'],
                    "nextTierProgress": progress_amount
                }
            }
            db.customers.update_one(email_query, new_values)
        else:
            # if there is no existing customer with that email, we add a new one to the db with appropriate calcualtions
            rewards_index = int((points_earned / 100)) - 1
            progress_amount = (points_earned % 100.) / 100.
            curr_tier = rewards[rewards_index if rewards_index < 9 else 9]
            next_tier = rewards[rewards_index + 1 if rewards_index < 9 else 9]

            # make new customer object and store it to the customers collection
            new_customer = {
                "email": email,
                "points": points_earned,
                "tier": curr_tier['tier'],
                "tierName": curr_tier['rewardName'],
                "nextTier": next_tier['tier'],
                "nextTierName": next_tier['rewardName'],
                "nextTierProgress": progress_amount
            }
            db.customers.insert(new_customer)
    get = post
