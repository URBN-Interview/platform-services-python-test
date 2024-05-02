import re
import json
import tornado.web
from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerHandler(tornado.web.RequestHandler):
    """
    Request handler for managing customer data.
    """

    @coroutine
    def get(self, email):
        """
        GET method to retrieve a customer's rewards data.

        Request Arguments:
        - email: Customer's email address

        Response:
        - 200 OK: Customer rewards data retrieved successfully
        - 400 Bad Request: Missing or invalid email address
        - 404 Not Found: Customer not found
        """

        # Validate email
        if not email or not self._is_valid_email(email):
            self.set_status(400)
            self.write("Missing or invalid email address")
            return

        # Retrieve customer rewards data from MongoDB (implementation required)
        rewards_data = self._retrieve_rewards_data(email)

        if rewards_data:
            # Respond with customer rewards data
            self.set_status(200)
            self.write(json.dumps(rewards_data))
        else:
            # Respond with customer not found
            self.set_status(404)
            self.write("Customer not found")

    def _retrieve_rewards_data(self, email):
        """
        Retrieve customer rewards data from MongoDB.

        Args:
            email (str): Customer's email address.

        Returns:
            dict: Customer rewards data if found, None otherwise.
        """
        # Connect to MongoDB
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        # Query MongoDB to retrieve customer rewards data
        reward = list(db.customers.find({"email": email}, {"_id": 0}))

        return reward

    def _is_valid_email(self, email):
        """
        Validate email address format.

        Args:
            email (str): Email address to validate.

        Returns:
            bool: True if the email address is valid, False otherwise.
        """
        # Regular expression for email validation
        regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(regex, email) is not None
