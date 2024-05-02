import requests

class RewardsServiceClient:
    """
    Client for interacting with the RewardsService API.
    """

    def __init__(self):
        """
        Initializes the RewardsServiceClient with base URLs for different endpoints.
        """
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.order_url = "http://rewardsservice:7050/orders"
        self.customers_url = "http://rewardsservice:7050/customers"

    def get_rewards(self):
        """
        Retrieves reward data from the RewardsService API.

        Returns:
            dict: Reward data as JSON.
        """
        response = requests.get(self.rewards_url)
        return response.json()

    def submit_order(self, email, total_amount):
        """
        Submits an order to the RewardsService API.

        Args:
            email (str): The customer's email address.
            total_amount (float): The total amount of the order.

        Returns:
            str: A message indicating the success or failure of the order submission.
        """
        order_data = {
            'email': email,
            'total_amount': int(total_amount)
        }
        try:
            response = requests.post(self.order_url, json=order_data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            if response.status_code == 200:
                return "Order submitted successfully."
            else:
                return "Failed to submit order. Please try again later."
        except requests.RequestException as e:
            return "Failed to submit order. Please try again later."

    def get_customers_rewards(self, email=None):
        """
        Retrieves customer rewards data from the RewardsService API.

        Args:
            email (str, optional): The customer's email address. If provided, retrieves rewards data for the specific customer. Defaults to None.

        Returns:
            dict: Customer rewards data as JSON.
        """
        if email:
            response = requests.get(self.customers_url + '/' + email)
        else:
            response = requests.get(self.customers_url)
        return response.json()