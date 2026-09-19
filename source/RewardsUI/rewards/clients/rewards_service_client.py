import requests


class RewardsServiceError(Exception):
    """Raised when the RewardsService can't fulfill a request."""

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        return str(self.args[0])


class RewardsServiceClient:

    def __init__(self, base_url="http://rewardsservice:7050"):
        self.base_url = base_url

    def get_rewards(self):
        return self._request("get", "/rewards")

    def get_all_customer_rewards(self):
        return self._request("get", "/rewards/customers")

    def get_customer_rewards(self, email):
        try:
            return self._request("get", "/rewards/customers/{}".format(email))
        except RewardsServiceError as e:
            if e.status_code == 404:
                return None
            raise

    def submit_order(self, email, order_total):
        return self._request(
            "post", "/rewards/orders", json={"email": email, "orderTotal": order_total}
        )

    def _request(self, method, path, **kwargs):
        try:
            response = requests.request(method, self.base_url + path, timeout=5, **kwargs)
        except requests.exceptions.RequestException as e:
            raise RewardsServiceError("Could not reach the rewards service") from e

        if not response.ok:
            message = response.text
            try:
                message = response.json().get("error", message)
            except ValueError:
                pass
            raise RewardsServiceError(message, status_code=response.status_code)

        return response.json()
