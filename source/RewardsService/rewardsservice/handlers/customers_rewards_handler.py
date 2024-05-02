import json
import tornado.web
from pymongo import MongoClient
from tornado.gen import coroutine


class CustomersRewardsHandler(tornado.web.RequestHandler):
    """
    Request handler for managing customers rewards data.
    """

    @coroutine
    def get(self):
        """
        GET method to retrieve rewards data for all customers.

        Request Arguments:
        - None

        Response:
        - 200 OK: Customers rewards data retrieved successfully
        """
        # Retrieve rewards data for all customers
        rewards_data = self._retrieve_rewards_data()

        # Respond with rewards data
        self.write(json.dumps(rewards_data))

    def _retrieve_rewards_data(self):
        """
        Retrieve rewards data for all customers from MongoDB.

        Returns:
            list: List of rewards data for all customers.
        """
        # Connect to MongoDB
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        # Retrieve rewards data for all customers
        rewards_data = list(db.customers.find({}, {"_id": 0}))

        return rewards_data