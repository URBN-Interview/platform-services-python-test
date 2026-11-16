# Unit tests for GET /rewards, using the same in-memory FakeDatabase as the
# orders tests (no MongoDB needed).
#
# Run from source/RewardsService:
#   docker compose exec rewardsservice python -m unittest discover -s tests -v

import json

import tornado.web
from tornado.testing import AsyncHTTPTestCase

from test_orders_endpoint import TIERS, FakeDatabase, url_patterns


class RewardsHandlerTest(AsyncHTTPTestCase):

    def get_app(self):
        app = tornado.web.Application(url_patterns)
        app.db = FakeDatabase()
        return app

    def test_returns_all_reward_tiers_as_json(self):
        response = self.fetch("/rewards")

        self.assertEqual(response.code, 200)
        self.assertIn("application/json", response.headers["Content-Type"])
        self.assertEqual(json.loads(response.body), TIERS)

    def test_post_is_not_allowed(self):
        response = self.fetch("/rewards", method="POST", body="{}")
        self.assertEqual(response.code, 405)
        self.assertIn("error", json.loads(response.body))
