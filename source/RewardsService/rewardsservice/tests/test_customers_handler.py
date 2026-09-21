import json

import tornado.testing
from mongomock_motor import AsyncMongoMockClient

from app import App
from url_patterns import url_patterns

CUSTOMER = {
    "email": "customer01@gmail.com",
    "rewardPoints": 100,
    "rewardTier": "A",
    "rewardTierName": "5% off purchase",
    "nextRewardTier": "B",
    "nextRewardTierName": "10% off purchase",
    "nextRewardTierProgress": 0.5,
}


class CustomersHandlerTests(tornado.testing.AsyncHTTPTestCase):

    def runTest(self):
        # pytest's fixture scanning instantiates this class with the
        # unittest default methodName ("runTest"); tornado's AsyncTestCase
        # __init__ requires that method to exist even though it's unused.
        pass

    def get_app(self):
        self.db = AsyncMongoMockClient()["Rewards"]
        return App(url_patterns, db=self.db)

    def test_list_all_customers_empty(self):
        response = self.fetch("/rewards/customers")
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), [])

    def test_list_all_customers(self):
        self.io_loop.run_sync(lambda: self.db.customerRewards.insert_one(dict(CUSTOMER)))

        response = self.fetch("/rewards/customers")

        self.assertEqual(response.code, 200)
        body = json.loads(response.body)
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["email"], "customer01@gmail.com")
        self.assertNotIn("_id", body[0])

    def test_get_single_customer_found(self):
        self.io_loop.run_sync(lambda: self.db.customerRewards.insert_one(dict(CUSTOMER)))

        response = self.fetch("/rewards/customers/customer01@gmail.com")

        self.assertEqual(response.code, 200)
        body = json.loads(response.body)
        self.assertEqual(body["rewardPoints"], 100)

    def test_get_single_customer_not_found(self):
        response = self.fetch("/rewards/customers/nobody@gmail.com")

        self.assertEqual(response.code, 404)
        self.assertIn("error", json.loads(response.body))

    def test_list_customers_filters_by_email_substring(self):
        self.io_loop.run_sync(lambda: self.db.customerRewards.insert_many([
            dict(CUSTOMER, email="customer01@gmail.com"),
            dict(CUSTOMER, email="customer04@gmail.com"),
            dict(CUSTOMER, email="someoneelse@gmail.com"),
        ]))

        response = self.fetch("/rewards/customers?email=customer0")

        self.assertEqual(response.code, 200)
        emails = {c["email"] for c in json.loads(response.body)}
        self.assertEqual(emails, {"customer01@gmail.com", "customer04@gmail.com"})

    def test_list_customers_filter_is_case_insensitive(self):
        self.io_loop.run_sync(
            lambda: self.db.customerRewards.insert_one(dict(CUSTOMER, email="Customer01@gmail.com"))
        )

        response = self.fetch("/rewards/customers?email=CUSTOMER01")

        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)), 1)

    def test_list_customers_filter_no_match_returns_empty_list(self):
        self.io_loop.run_sync(lambda: self.db.customerRewards.insert_one(dict(CUSTOMER)))

        response = self.fetch("/rewards/customers?email=nobody")

        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), [])

    def test_list_customers_filter_escapes_regex_metacharacters(self):
        self.io_loop.run_sync(lambda: self.db.customerRewards.insert_one(dict(CUSTOMER)))

        response = self.fetch("/rewards/customers?email=" + "customer01.*")

        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), [])
