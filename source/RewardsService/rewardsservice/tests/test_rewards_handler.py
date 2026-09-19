import json

import tornado.testing
from mongomock_motor import AsyncMongoMockClient

from app import App
from url_patterns import url_patterns

TIERS = [
    {"tier": "A", "rewardName": "5% off purchase", "points": 100},
    {"tier": "B", "rewardName": "10% off purchase", "points": 200},
]


class RewardsHandlerTests(tornado.testing.AsyncHTTPTestCase):

    def runTest(self):
        # pytest's fixture scanning instantiates this class with the
        # unittest default methodName ("runTest"); tornado's AsyncTestCase
        # __init__ requires that method to exist even though it's unused.
        pass

    def get_app(self):
        self.db = AsyncMongoMockClient()["Rewards"]
        return App(url_patterns, db=self.db)

    def test_get_rewards_returns_tier_list(self):
        self.io_loop.run_sync(lambda: self.db.rewards.insert_many(TIERS))

        response = self.fetch("/rewards")

        self.assertEqual(response.code, 200)
        body = json.loads(response.body)
        self.assertEqual(len(body), 2)
        self.assertEqual(body[0]["tier"], "A")
        self.assertNotIn("_id", body[0])

    def test_get_rewards_empty_collection(self):
        response = self.fetch("/rewards")

        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), [])
