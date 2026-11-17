import logging
from urllib.parse import quote

import requests

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "http://rewardsservice:7050"


class RewardsServiceError(Exception):
    """Raised when the RewardsService cannot be reached or rejects a request."""

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class RewardsServiceClient:

    def __init__(self, base_url=DEFAULT_BASE_URL, timeout=5, session=None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()

    def get_rewards(self):
        return self._request("GET", "/rewards")

    def get_customers(self):
        return self._request("GET", "/customers")

    def get_customer(self, email):
        """Return the customer's rewards data, or None if the customer doesn't exist."""
        try:
            return self._request("GET", "/customers/{}".format(quote(email, safe="")))
        except RewardsServiceError as e:
            if e.status_code == 404:
                return None
            raise

    def add_order(self, email, order_total):
        return self._request("POST", "/orders", json={"email": email, "orderTotal": order_total})

    def _request(self, method, path, **kwargs):
        url = self.base_url + path
        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        except requests.RequestException:
            logger.exception("Error calling RewardsService %s %s", method, url)
            raise RewardsServiceError("The rewards service is unavailable. Please try again later.")

        if response.ok:
            return response.json()

        raise RewardsServiceError(self._error_message(response), status_code=response.status_code)

    @staticmethod
    def _error_message(response):
        try:
            return response.json()["error"]["message"]
        except (ValueError, KeyError, TypeError):
            return "The rewards service returned an error ({}).".format(response.status_code)
