import json
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING, MongoClient

from tornado.escape import json_encode, json_decode
from tornado.gen import coroutine
import tornado.web


class CustomerRewardsHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.client = MongoClient("mongodb", 27017)
        self.db = self.client['Rewards']

    @staticmethod
    def _calculate_points(amount, available_points=0):
        """
        Method to return calculated points based on user available points and amount i.e. $1 = 1 points.

        Args:
            amount (float): order total amount.
            available_points (int): user available points

        Returns:
            It returns calculated reward points based on user available points and amount.
        """
        return available_points + int(amount or 0)

    def _calculate_progress(self, points):
        """
        Method to calculate user reward program progress status. It will return completed percent of user reward program
        between previous and next reward program.

        Args:
            points (int): user aggregated rewards points

        Returns:
            It returns user reward program completed percentage.
        """
        top_reward_prg = self.get_top_reward()
        if points > top_reward_prg.get("points"):
            return 100
        curr_reward_prg = self.get_current_reward_program(points)
        nxt_reward_prg = self.get_next_reward_program(points)
        diff = nxt_reward_prg.get("points") - curr_reward_prg.get("points", 0)
        rem = points % 100 if points > 100 else points
        return round((rem/diff) * 100, 2)

    def get_customer_available_points(self, email):
        """
        Method to get customer available points. It will do aggregation query to get customer total earned reward points.

        Args:
            email (char): aggregate customer reward points based on unique email id.

        Returns:
            It returns customer available reward points.
        """
        customer = self.db.customers.aggregate([
            {
                "$group": {
                    "_id": "$emailId",
                    "totalPoints": {"$sum": "$earnedPoints"},
                },
            },
            {
                "$match": {"_id": email}
            }
        ])
        customer = list(customer)
        return customer[0].get("totalPoints") if customer else 0

    def get_top_reward(self):
        """
        Method to get top reward program from rewards collection based on highest points document.

        Returns:
            It return reward program document in dict format.
        """
        return self.db.rewards.find_one({}, sort=[("points", DESCENDING)]) or {}

    def get_current_reward_program(self, points):
        """
        Method to return current reward program document based on the customer accumulated points.

        Returns:
            It return reward program document in dict format.
        """
        top_reward_prg = self.get_top_reward()
        if points > top_reward_prg.get("points"):
            return top_reward_prg
        lower_bound = points - 100
        return self.db.rewards.find_one({
            "$and": [{"points": {"$gt": lower_bound}}, {"points": {"$lte": points}}]
        }) or {}

    def get_next_reward_program(self, points):
        """
        Method to return next available reward program document based on the customer accumulated points.

        Returns:
            It return reward program document in dict format.
        """
        top_reward_prg = self.get_top_reward()
        if points > top_reward_prg.get("points"):
            return top_reward_prg
        upper_bound = points + 100
        return self.db.rewards.find_one({
            "$and": [{"points": {"$gt": points}}, {"points": {"$lte": upper_bound}}]
        }) or {}

    @coroutine
    def post(self):
        try:
            customer = json_decode(self.request.body)
            available_points = self.get_customer_available_points(customer.get("emailId"))
            top_reward_prg = self.get_top_reward()
            # Once customer has reached top rewards tier, there are no more rewards the customer can earn.
            if available_points < top_reward_prg.get("points"):
                points = self._calculate_points(customer.get("orderTotal"), available_points)
                curr_reward_prg = self.get_current_reward_program(points)
                nxt_reward_prg = self.get_next_reward_program(points)
                customer.update({
                    "_id": str(ObjectId()),
                    "earnedPoints": int(customer.get("orderTotal") or 0),
                    "points": points,
                    "tier": curr_reward_prg.get("tier"),
                    "rewardName": curr_reward_prg.get("rewardName"),
                    "nextTier": nxt_reward_prg.get("tier"),
                    "nextRewardName": nxt_reward_prg.get("rewardName"),
                    "nextRewardTierAwayPercentage": (100 - self._calculate_progress(points)),  # Away from next program
                })

                del customer["orderTotal"]
                self.db.customers.insert_one(customer)
                self.set_status(201)
                self.write(json_encode({"message": "Customer rewards created successfully!"}))
            else:
                self.set_status(200)
                self.write(json_encode({"message": "You cann't earn more rewards as you reach to the top."}))
        except Exception as e:
            err_msg = "Error while creating customer rewards: {}".format(e)
            self.set_status(500)
            self.write(json_encode({"message": err_msg}))

    @coroutine
    def get(self):
        try:
            email = self.get_argument("email", None, True)
            condition = {"emailId": email} if email else {}
            customers = list(self.db.customers.find(condition).sort([("emailId", ASCENDING), ("points", ASCENDING)]))
            self.set_status(200)
            self.write(json.dumps(customers))
        except Exception as e:
            err_msg = "Error while getting customer rewards: {}".format(e)
            self.set_status(500)
            self.write(json_encode({"message": err_msg}))
