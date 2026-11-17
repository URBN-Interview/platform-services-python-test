import json
import unittest

from pymongo.errors import ServerSelectionTimeoutError
from tornado.testing import AsyncHTTPTestCase

import rewards_calculator
from app import App

TIERS = [
    {"tier": chr(ord("A") + i), "rewardName": "{}% off purchase".format(5 * (i + 1)), "points": 100 * (i + 1)}
    for i in range(10)
]


class FakeRepository:
    """In-memory stand-in for RewardsRepository."""

    def __init__(self):
        self.customers = {}
        self.fail = False

    def _check(self):
        if self.fail:
            raise ServerSelectionTimeoutError("mongo down")

    async def get_tiers(self):
        self._check()
        return list(TIERS)

    async def get_customer(self, email):
        self._check()
        return self.customers.get(email)

    async def get_customers(self):
        self._check()
        return [self.customers[email] for email in sorted(self.customers)]

    async def add_order(self, email, order_total):
        self._check()
        current = self.customers.get(email, {}).get("points", 0)
        points = current + rewards_calculator.points_for_order(order_total)
        self.customers[email] = rewards_calculator.calculate_rewards(email, points, TIERS)
        return self.customers[email]


class HandlerTestCase(AsyncHTTPTestCase):

    def get_app(self):
        self.repository = FakeRepository()
        return App(self.repository, debug=False)

    def request(self, method, path, body=None):
        if body is not None and not isinstance(body, str):
            body = json.dumps(body)
        response = self.fetch(path, method=method, body=body)
        return response, json.loads(response.body) if response.body else None

    def post_order(self, email, order_total):
        return self.request("POST", "/orders", {"email": email, "orderTotal": order_total})


class RewardsHandlerTest(HandlerTestCase):

    def test_lists_tiers(self):
        response, body = self.request("GET", "/rewards")
        self.assertEqual(response.code, 200)
        self.assertEqual(body, TIERS)
        self.assertIn("application/json", response.headers["Content-Type"])


class OrdersHandlerTest(HandlerTestCase):

    def test_creates_customer_rewards(self):
        response, body = self.post_order("Customer01@gmail.com", 100.80)
        self.assertEqual(response.code, 201)
        self.assertEqual(response.headers["Location"], "/customers/customer01@gmail.com")
        self.assertEqual(body, {
            "email": "customer01@gmail.com",
            "points": 100,
            "tier": "A",
            "tierName": "5% off purchase",
            "nextTier": "B",
            "nextTierName": "10% off purchase",
            "nextTierProgress": 0.5,
        })

    def test_accumulates_points_across_orders(self):
        self.post_order("c@x.com", 150)
        _, body = self.post_order("c@x.com", "75.50")
        self.assertEqual(body["points"], 225)
        self.assertEqual(body["tier"], "B")

    def test_caps_at_top_tier(self):
        self.post_order("c@x.com", 999.99)
        _, body = self.post_order("c@x.com", 5000)
        self.assertEqual(body["points"], 1000)
        self.assertEqual(body["tier"], "J")
        self.assertIsNone(body["nextTier"])

    def test_validation_errors(self):
        cases = [
            "not json",
            "[1, 2]",
            {"orderTotal": 10},
            {"email": "c@x.com"},
            {"email": "bad-email", "orderTotal": 10},
            {"email": "c@x.com", "orderTotal": -5},
            {"email": "c@x.com", "orderTotal": "abc"},
        ]
        for body in cases:
            with self.subTest(body=body):
                response, payload = self.request("POST", "/orders", body)
                self.assertEqual(response.code, 400)
                self.assertEqual(payload["error"]["code"], 400)
                self.assertTrue(payload["error"]["message"])
        self.assertEqual(self.repository.customers, {})

    def test_get_not_allowed(self):
        response, _ = self.request("GET", "/orders")
        self.assertEqual(response.code, 405)


class CustomersHandlerTest(HandlerTestCase):

    def test_get_customer(self):
        self.post_order("c@x.com", 450)
        response, body = self.request("GET", "/customers/C@X.com")
        self.assertEqual(response.code, 200)
        self.assertEqual(body["email"], "c@x.com")
        self.assertEqual(body["tier"], "D")

    def test_get_url_encoded_customer(self):
        self.post_order("first+last@x.com", 10)
        response, body = self.request("GET", "/customers/first%2Blast%40x.com")
        self.assertEqual(response.code, 200)
        self.assertEqual(body["email"], "first+last@x.com")

    def test_unknown_customer_is_404(self):
        response, body = self.request("GET", "/customers/nobody@x.com")
        self.assertEqual(response.code, 404)
        self.assertIn("not found", body["error"]["message"])

    def test_invalid_email_is_400(self):
        response, _ = self.request("GET", "/customers/not-an-email")
        self.assertEqual(response.code, 400)

    def test_list_customers(self):
        _, body = self.request("GET", "/customers")
        self.assertEqual(body, [])

        self.post_order("b@x.com", 100)
        self.post_order("a@x.com", 200)
        response, body = self.request("GET", "/customers")
        self.assertEqual(response.code, 200)
        self.assertEqual([c["email"] for c in body], ["a@x.com", "b@x.com"])

    def test_database_unavailable_is_503(self):
        self.repository.fail = True
        response, body = self.request("GET", "/customers")
        self.assertEqual(response.code, 503)
        self.assertIn("unavailable", body["error"]["message"])


if __name__ == "__main__":
    unittest.main()
