import json
import os
import sys
import unittest

import tornado.web
from tornado.testing import AsyncHTTPTestCase

# url_patterns uses the same imports as app.py, which expect rewardsservice/ on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "rewardsservice"))
from url_patterns import build_url_patterns

TIERS = [
    {"tier": "A", "rewardName": "5% off purchase", "points": 100},
    {"tier": "B", "rewardName": "10% off purchase", "points": 200},
    {"tier": "C", "rewardName": "15% off purchase", "points": 300},
]


class FakeRewardsRepo:
    async def get_all_tiers(self):
        return TIERS


class FakeCustomersRepo:
    def __init__(self):
        self.customers = {}

    async def get_customer(self, email):
        return self.customers.get(email)

    async def update_customer(self, email, new_values):
        self.customers[email] = {"email_address": email, **new_values}
        return self.customers[email]

    async def get_all_customers(self):
        return list(self.customers.values())


class TestHandlers(AsyncHTTPTestCase):
    def get_app(self):
        self.customers_repo = FakeCustomersRepo()
        return tornado.web.Application(build_url_patterns(FakeRewardsRepo(), self.customers_repo))

    def post_order(self, body):
        return self.fetch("/customer", method="POST", body=body)

    def test_get_rewards(self):
        response = self.fetch("/rewards")
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), TIERS)

    def test_post_order_for_new_customer(self):
        response = self.post_order('{"email_address": "a@b.com", "order_total": 150.99}')
        self.assertEqual(response.code, 201)
        self.assertEqual(json.loads(response.body), {
            "email_address": "a@b.com",
            "reward_points": 150,
            "reward_tier": "A",
            "reward_tier_name": "5% off purchase",
            "next_reward_tier": "B",
            "next_reward_tier_name": "10% off purchase",
            "next_reward_tier_progress": 0.5,
        })

    def test_post_order_adds_to_existing_points(self):
        self.post_order('{"email_address": "a@b.com", "order_total": 100}')
        response = self.post_order('{"email_address": "a@b.com", "order_total": 150}')
        body = json.loads(response.body)
        self.assertEqual(body["reward_points"], 250)
        self.assertEqual(body["reward_tier"], "B")

    def test_post_order_invalid_body(self):
        response = self.post_order("not json")
        self.assertEqual(response.code, 400)
        self.assertEqual(json.loads(response.body), {
            "error": {"status": 400, "message": "request body must be valid JSON"},
        })

    def test_get_customer(self):
        self.customers_repo.customers["a@b.com"] = {"email_address": "a@b.com", "reward_points": 150}
        response = self.fetch("/customer/a@b.com")
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), {"email_address": "a@b.com", "reward_points": 150})

    def test_get_missing_customer(self):
        response = self.fetch("/customer/nobody@b.com")
        self.assertEqual(response.code, 404)
        self.assertEqual(json.loads(response.body), {
            "error": {"status": 404, "message": "customer not found"},
        })

    def test_get_all_customers(self):
        self.post_order('{"email_address": "a@b.com", "order_total": 100}')
        self.post_order('{"email_address": "c@d.com", "order_total": 200}')
        response = self.fetch("/customers")
        self.assertEqual(response.code, 200)
        emails = [c["email_address"] for c in json.loads(response.body)]
        self.assertEqual(emails, ["a@b.com", "c@d.com"])


if __name__ == "__main__":
    unittest.main()
