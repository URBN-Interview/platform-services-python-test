# Unit tests for Endpoint 2 (GET /customers/{email}) and Endpoint 3 (GET /customers),
# using the same in-memory FakeDatabase as the orders tests (no MongoDB needed).
#
# Run from source/RewardsService:
#   docker compose exec rewardsservice python -m unittest discover -s tests -v

import json

import tornado.web
from tornado.testing import AsyncHTTPTestCase

from test_orders_endpoint import FakeDatabase, url_patterns


CUSTOMER_01 = {
    "emailAddress": "customer01@gmail.com",
    "rewardPoints": 250,
    "rewardTier": "B",
    "rewardTierName": "10% off purchase",
    "nextRewardTier": "C",
    "nextRewardTierName": "15% off purchase",
    "nextRewardTierProgress": 0.5,
}


class CustomerHandlerTest(AsyncHTTPTestCase):

    def get_app(self):
        app = tornado.web.Application(url_patterns)
        app.db = FakeDatabase()
        self.db = app.db
        return app

    def post_order(self, email, order_total):
        return self.fetch("/orders", method="POST",
                          body=json.dumps({"email": email, "orderTotal": order_total}))

    # --- found ---

    def test_returns_stored_rewards_for_customer(self):
        self.post_order("customer01@gmail.com", 250)
        response = self.fetch("/customers/customer01@gmail.com")

        self.assertEqual(response.code, 200)
        self.assertIn("application/json", response.headers["Content-Type"])
        self.assertEqual(json.loads(response.body), CUSTOMER_01)

    def test_matches_what_post_orders_returned(self):
        posted = json.loads(self.post_order("customer01@gmail.com", 1234.56).body)
        fetched = json.loads(self.fetch("/customers/customer01@gmail.com").body)
        self.assertEqual(fetched, posted)

    def test_does_not_return_mongo_id(self):
        self.post_order("customer01@gmail.com", 250)
        body = json.loads(self.fetch("/customers/customer01@gmail.com").body)
        self.assertNotIn("_id", body)

    def test_lookup_is_case_insensitive(self):
        self.post_order("customer01@gmail.com", 250)
        response = self.fetch("/customers/Customer01@GMAIL.com")

        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)["emailAddress"], "customer01@gmail.com")

    def test_url_encoded_email(self):
        self.post_order("customer01@gmail.com", 250)
        self.assertEqual(self.fetch("/customers/customer01%40gmail.com").code, 200)

    def test_email_with_plus_sign(self):
        self.post_order("first+promo@gmail.com", 250)

        self.assertEqual(self.fetch("/customers/first+promo@gmail.com").code, 200)
        self.assertEqual(self.fetch("/customers/first%2Bpromo@gmail.com").code, 200)

    def test_returns_only_the_requested_customer(self):
        self.post_order("customer01@gmail.com", 250)
        self.post_order("customer02@gmail.com", 900)

        body = json.loads(self.fetch("/customers/customer02@gmail.com").body)
        self.assertEqual(body["emailAddress"], "customer02@gmail.com")
        self.assertEqual(body["rewardPoints"], 900)

    # --- not found / bad requests ---

    def test_unknown_customer_returns_404_json(self):
        response = self.fetch("/customers/nobody@gmail.com")

        self.assertEqual(response.code, 404)
        self.assertIn("application/json", response.headers["Content-Type"])
        self.assertEqual(json.loads(response.body), {"error": "Customer not found"})

    def test_blank_email_returns_400(self):
        self.assertEqual(self.fetch("/customers/%20%20").code, 400)

    def test_post_is_not_allowed(self):
        self.post_order("customer01@gmail.com", 250)
        response = self.fetch("/customers/customer01@gmail.com", method="POST", body="{}")
        self.assertEqual(response.code, 405)


class CustomersHandlerTest(AsyncHTTPTestCase):
    """Endpoint 3: GET /customers"""

    def get_app(self):
        app = tornado.web.Application(url_patterns)
        app.db = FakeDatabase()
        self.db = app.db
        return app

    def post_order(self, email, order_total):
        return self.fetch("/orders", method="POST",
                          body=json.dumps({"email": email, "orderTotal": order_total}))

    def get_customers(self):
        response = self.fetch("/customers")
        return response, json.loads(response.body)

    def test_no_customers_returns_empty_list(self):
        response, body = self.get_customers()

        self.assertEqual(response.code, 200)
        self.assertIn("application/json", response.headers["Content-Type"])
        self.assertEqual(body, [])

    def test_returns_customer_rewards_data(self):
        self.post_order("customer01@gmail.com", 250)
        response, body = self.get_customers()

        self.assertEqual(response.code, 200)
        self.assertEqual(body, [CUSTOMER_01])

    def test_items_match_single_customer_endpoint(self):
        self.post_order("customer01@gmail.com", 250)
        self.post_order("customer02@gmail.com", 1234.56)

        _, body = self.get_customers()
        for customer in body:
            single = json.loads(self.fetch("/customers/" + customer["emailAddress"]).body)
            self.assertEqual(customer, single)

    def test_returns_all_customers_sorted_by_email(self):
        for email in ("charlie@gmail.com", "alice@gmail.com", "bob@gmail.com"):
            self.post_order(email, 100)

        _, body = self.get_customers()
        self.assertEqual([c["emailAddress"] for c in body],
                         ["alice@gmail.com", "bob@gmail.com", "charlie@gmail.com"])

    def test_customer_with_multiple_orders_appears_once(self):
        self.post_order("customer01@gmail.com", 150)
        self.post_order("customer01@gmail.com", 150)

        _, body = self.get_customers()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["rewardPoints"], 300)

    def test_does_not_return_mongo_id(self):
        self.post_order("customer01@gmail.com", 250)
        self.post_order("customer02@gmail.com", 500)

        _, body = self.get_customers()
        for customer in body:
            self.assertNotIn("_id", customer)

    def test_post_is_not_allowed(self):
        response = self.fetch("/customers", method="POST", body="{}")
        self.assertEqual(response.code, 405)
        self.assertIn("error", json.loads(response.body))
