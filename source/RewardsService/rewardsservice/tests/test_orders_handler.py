import json

import tornado.testing
from mongomock_motor import AsyncMongoMockClient

from app import App
from url_patterns import url_patterns

TIERS = [
    {"tier": "A", "rewardName": "5% off purchase", "points": 100},
    {"tier": "B", "rewardName": "10% off purchase", "points": 200},
]


class OrdersHandlerTests(tornado.testing.AsyncHTTPTestCase):

    def runTest(self):
        # pytest's fixture scanning instantiates this class with the
        # unittest default methodName ("runTest"); tornado's AsyncTestCase
        # __init__ requires that method to exist even though it's unused.
        pass

    def get_app(self):
        self.db = AsyncMongoMockClient()["Rewards"]
        self.io_loop.run_sync(lambda: self.db.rewards.insert_many(TIERS))
        return App(url_patterns, db=self.db)

    def post_order(self, email, order_total):
        return self.fetch(
            "/rewards/orders",
            method="POST",
            body=json.dumps({"email": email, "orderTotal": order_total}),
        )

    def test_new_customer_order_is_calculated_and_stored(self):
        response = self.post_order("customer01@gmail.com", 100.80)

        self.assertEqual(response.code, 201)
        body = json.loads(response.body)
        self.assertEqual(body["email"], "customer01@gmail.com")
        self.assertEqual(body["rewardPoints"], 100)
        self.assertEqual(body["rewardTier"], "A")
        self.assertEqual(body["nextRewardTier"], "B")
        self.assertEqual(body["nextRewardTierProgress"], 0.5)

        stored = self.io_loop.run_sync(
            lambda: self.db.customerRewards.find_one({"email": "customer01@gmail.com"})
        )
        self.assertEqual(stored["rewardPoints"], 100)

    def test_points_accumulate_across_orders(self):
        self.post_order("customer01@gmail.com", 100.80)
        response = self.post_order("customer01@gmail.com", 50)

        body = json.loads(response.body)
        self.assertEqual(body["rewardPoints"], 150)
        self.assertEqual(body["rewardTier"], "A")
        self.assertEqual(body["nextRewardTierProgress"], 0.75)

    def test_missing_email_returns_400(self):
        response = self.fetch(
            "/rewards/orders",
            method="POST",
            body=json.dumps({"orderTotal": 10}),
        )
        self.assertEqual(response.code, 400)
        self.assertIn("error", json.loads(response.body))

    def test_invalid_email_returns_400(self):
        response = self.post_order("not-an-email", 10)
        self.assertEqual(response.code, 400)

    def test_negative_order_total_returns_400(self):
        response = self.post_order("customer01@gmail.com", -5)
        self.assertEqual(response.code, 400)

    def test_zero_order_total_returns_400(self):
        response = self.post_order("customer01@gmail.com", 0)
        self.assertEqual(response.code, 400)

    def test_non_numeric_order_total_returns_400(self):
        response = self.post_order("customer01@gmail.com", "abc")
        self.assertEqual(response.code, 400)

    def test_malformed_json_body_returns_400(self):
        response = self.fetch("/rewards/orders", method="POST", body="not json")
        self.assertEqual(response.code, 400)
