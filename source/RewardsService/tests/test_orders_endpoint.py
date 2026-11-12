# Unit tests for Endpoint 1: POST /orders and the rewards calculator behind it.
#
# The handler tests run the real Tornado routes against an in-memory FakeDatabase,
# so MongoDB does not need to be running and tests never touch real data.
#
# Run from source/RewardsService (inside the container, where Tornado is installed):
#   docker compose exec rewardsservice python -m unittest discover -s tests -v

import copy
import json
import os
import sys
import unittest

import tornado.web
from tornado.testing import AsyncHTTPTestCase

# The app imports its modules as top-level names (e.g. `from handlers...`),
# so put the rewardsservice/ folder on the import path.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "rewardsservice"))

from rewards_calculator import calculate_rewards, points_for_order  # noqa: E402
from url_patterns import url_patterns  # noqa: E402


TIERS = [
    {"tier": "A", "rewardName": "5% off purchase", "points": 100},
    {"tier": "B", "rewardName": "10% off purchase", "points": 200},
    {"tier": "C", "rewardName": "15% off purchase", "points": 300},
    {"tier": "D", "rewardName": "20% off purchase", "points": 400},
    {"tier": "E", "rewardName": "25% off purchase", "points": 500},
    {"tier": "F", "rewardName": "30% off purchase", "points": 600},
    {"tier": "G", "rewardName": "35% off purchase", "points": 700},
    {"tier": "H", "rewardName": "40% off purchase", "points": 800},
    {"tier": "I", "rewardName": "45% off purchase", "points": 900},
    {"tier": "J", "rewardName": "50% off purchase", "points": 1000},
]


# ---------------------------------------------------------------------------
# In-memory stand-in for the Motor database
# ---------------------------------------------------------------------------

class FakeCursor:
    """Mimics a Motor cursor: supports sort() and to_list()."""

    def __init__(self, docs):
        self._docs = docs

    def sort(self, key, direction=1):
        self._docs = sorted(self._docs, key=lambda d: d.get(key), reverse=direction < 0)
        return self

    async def to_list(self, length):
        return copy.deepcopy(self._docs)


class FakeObjectId:
    """Stands in for Mongo's ObjectId: like the real one, json.dumps can't serialize it,
    so a handler that forgets to exclude _id fails in tests too."""


class FakeCollection:
    """Supports the subset of Motor's collection API the handlers use."""

    def __init__(self, docs=None):
        self.docs = copy.deepcopy(docs or [])

    @staticmethod
    def _matches(doc, query):
        return all(doc.get(k) == v for k, v in query.items())

    @staticmethod
    def _project(doc, projection):
        # Only exclusion projections like {"_id": 0} are needed
        excluded = {k for k, v in (projection or {}).items() if not v}
        return {k: copy.deepcopy(v) for k, v in doc.items() if k not in excluded}

    def find(self, query=None, projection=None):
        return FakeCursor([self._project(d, projection)
                           for d in self.docs if self._matches(d, query or {})])

    async def find_one(self, query, projection=None):
        for doc in self.docs:
            if self._matches(doc, query):
                return self._project(doc, projection)
        return None

    async def update_one(self, query, update, upsert=False):
        for doc in self.docs:
            if self._matches(doc, query):
                doc.update(copy.deepcopy(update["$set"]))
                return
        if upsert:
            # Like MongoDB, a newly inserted document gets an _id
            new_doc = {"_id": FakeObjectId()}
            new_doc.update(query)
            new_doc.update(copy.deepcopy(update["$set"]))
            self.docs.append(new_doc)


class FakeDatabase:
    def __init__(self):
        self.rewards = FakeCollection(TIERS)
        self.customers = FakeCollection()


# ---------------------------------------------------------------------------
# Calculator tests (pure logic, no HTTP or database)
# ---------------------------------------------------------------------------

class PointsForOrderTest(unittest.TestCase):

    def test_drops_cents(self):
        self.assertEqual(points_for_order(100.80), 100)

    def test_whole_dollars(self):
        self.assertEqual(points_for_order(250), 250)

    def test_under_one_dollar_is_zero(self):
        self.assertEqual(points_for_order(0.99), 0)

    def test_avoids_float_rounding_errors(self):
        # Floats can't represent most decimals exactly; whole dollars must never be lost
        self.assertEqual(points_for_order(4.35), 4)
        self.assertEqual(points_for_order(1000.00), 1000)


class CalculateRewardsTest(unittest.TestCase):

    def assertRewards(self, points, tier, next_tier, progress, stored_points=None):
        result = calculate_rewards(points, TIERS)
        self.assertEqual(result["rewardPoints"], points if stored_points is None else stored_points)
        self.assertEqual(result["rewardTier"], tier)
        self.assertEqual(result["nextRewardTier"], next_tier)
        self.assertEqual(result["nextRewardTierProgress"], progress)

    def test_zero_points_has_no_tier(self):
        self.assertRewards(0, None, "A", 0.0)

    def test_below_first_tier(self):
        self.assertRewards(50, None, "A", 0.5)

    def test_exactly_on_a_tier_boundary(self):
        self.assertRewards(100, "A", "B", 0.0)

    def test_halfway_between_tiers(self):
        self.assertRewards(250, "B", "C", 0.5)

    def test_one_point_below_top_tier(self):
        self.assertRewards(999, "I", "J", 0.99)

    def test_top_tier_has_no_next_tier(self):
        self.assertRewards(1000, "J", None, None)

    def test_points_capped_at_top_tier(self):
        self.assertRewards(1500, "J", None, None, stored_points=1000)

    def test_includes_tier_names(self):
        result = calculate_rewards(250, TIERS)
        self.assertEqual(result["rewardTierName"], "10% off purchase")
        self.assertEqual(result["nextRewardTierName"], "15% off purchase")

    def test_tier_order_from_database_does_not_matter(self):
        shuffled = list(reversed(TIERS))
        self.assertEqual(calculate_rewards(250, shuffled), calculate_rewards(250, TIERS))

    def test_does_not_modify_the_tiers_passed_in(self):
        shuffled = list(reversed(TIERS))
        before = copy.deepcopy(shuffled)
        calculate_rewards(250, shuffled)
        self.assertEqual(shuffled, before)


# ---------------------------------------------------------------------------
# Handler tests: real HTTP requests to POST /orders
# ---------------------------------------------------------------------------

class OrdersHandlerTest(AsyncHTTPTestCase):

    def get_app(self):
        app = tornado.web.Application(url_patterns)
        app.db = FakeDatabase()
        self.db = app.db
        return app

    def post_order(self, body):
        """POST to /orders. Dicts are sent as JSON; strings are sent as-is."""
        raw = body if isinstance(body, str) else json.dumps(body)
        return self.fetch("/orders", method="POST", body=raw,
                          headers={"Content-Type": "application/json"})

    # --- happy path ---

    def test_new_customer_returns_201_with_rewards(self):
        response = self.post_order({"email": "customer01@gmail.com", "orderTotal": 100.80})

        self.assertEqual(response.code, 201)
        self.assertEqual(json.loads(response.body), {
            "emailAddress": "customer01@gmail.com",
            "rewardPoints": 100,
            "rewardTier": "A",
            "rewardTierName": "5% off purchase",
            "nextRewardTier": "B",
            "nextRewardTierName": "10% off purchase",
            "nextRewardTierProgress": 0.0,
        })
        self.assertIn("application/json", response.headers["Content-Type"])

    def test_new_customer_is_stored(self):
        self.post_order({"email": "customer01@gmail.com", "orderTotal": 250})

        self.assertEqual(len(self.db.customers.docs), 1)
        stored = self.db.customers.docs[0]
        self.assertEqual(stored["emailAddress"], "customer01@gmail.com")
        self.assertEqual(stored["rewardPoints"], 250)
        self.assertEqual(stored["rewardTier"], "B")

    def test_points_accumulate_across_orders(self):
        self.post_order({"email": "customer01@gmail.com", "orderTotal": 150})
        response = self.post_order({"email": "customer01@gmail.com", "orderTotal": 150.99})

        body = json.loads(response.body)
        self.assertEqual(body["rewardPoints"], 300)
        self.assertEqual(body["rewardTier"], "C")
        # still one document per customer
        self.assertEqual(len(self.db.customers.docs), 1)

    def test_customers_are_kept_separate(self):
        self.post_order({"email": "customer01@gmail.com", "orderTotal": 150})
        self.post_order({"email": "customer02@gmail.com", "orderTotal": 500})

        self.assertEqual(len(self.db.customers.docs), 2)
        response = self.post_order({"email": "customer01@gmail.com", "orderTotal": 0})
        self.assertEqual(json.loads(response.body)["rewardPoints"], 150)

    def test_points_capped_at_top_tier_across_orders(self):
        self.post_order({"email": "customer01@gmail.com", "orderTotal": 800})
        response = self.post_order({"email": "customer01@gmail.com", "orderTotal": 800})

        body = json.loads(response.body)
        self.assertEqual(body["rewardPoints"], 1000)
        self.assertEqual(body["rewardTier"], "J")
        self.assertIsNone(body["nextRewardTier"])
        self.assertIsNone(body["nextRewardTierProgress"])

    def test_email_is_normalized(self):
        self.post_order({"email": "  Customer01@Gmail.COM ", "orderTotal": 100})
        response = self.post_order({"email": "customer01@gmail.com", "orderTotal": 100})

        body = json.loads(response.body)
        self.assertEqual(body["emailAddress"], "customer01@gmail.com")
        self.assertEqual(body["rewardPoints"], 200)
        self.assertEqual(len(self.db.customers.docs), 1)

    def test_zero_dollar_order_is_allowed(self):
        response = self.post_order({"email": "customer01@gmail.com", "orderTotal": 0})

        self.assertEqual(response.code, 201)
        self.assertEqual(json.loads(response.body)["rewardPoints"], 0)

    # --- bad requests ---

    def test_invalid_json_returns_400(self):
        self.assertEqual(self.post_order("not json").code, 400)

    def test_missing_email_returns_400(self):
        self.assertEqual(self.post_order({"orderTotal": 100}).code, 400)

    def test_missing_order_total_returns_400(self):
        self.assertEqual(self.post_order({"email": "customer01@gmail.com"}).code, 400)

    def test_empty_body_returns_400(self):
        self.assertEqual(self.post_order({}).code, 400)

    def test_bad_request_does_not_store_anything(self):
        self.post_order({"email": "customer01@gmail.com"})
        self.assertEqual(self.db.customers.docs, [])

    def test_get_is_not_allowed(self):
        self.assertEqual(self.fetch("/orders").code, 405)

    def test_body_must_be_a_json_object(self):
        self.assertEqual(self.post_order("[1, 2, 3]").code, 400)
        self.assertEqual(self.post_order("5").code, 400)

    def test_non_string_email_returns_400(self):
        self.assertEqual(self.post_order({"email": 12345, "orderTotal": 100}).code, 400)

    def test_blank_email_returns_400(self):
        self.assertEqual(self.post_order({"email": "   ", "orderTotal": 100}).code, 400)

    def test_email_format_is_not_checked(self):
        # Deliberate decision: only a non-empty string is required, not a full email check
        self.assertEqual(self.post_order({"email": "not-an-email", "orderTotal": 100}).code, 201)

    def test_non_numeric_order_total_returns_400(self):
        self.assertEqual(self.post_order({"email": "customer01@gmail.com", "orderTotal": "abc"}).code, 400)

    def test_numeric_string_order_total_returns_400(self):
        self.assertEqual(self.post_order({"email": "customer01@gmail.com", "orderTotal": "100"}).code, 400)

    def test_boolean_order_total_returns_400(self):
        self.assertEqual(self.post_order({"email": "customer01@gmail.com", "orderTotal": True}).code, 400)

    def test_negative_order_total_returns_400(self):
        self.assertEqual(self.post_order({"email": "customer01@gmail.com", "orderTotal": -50}).code, 400)

    def test_nan_and_infinity_order_total_return_400(self):
        for value in ("NaN", "Infinity", "1e999"):
            body = '{"email": "customer01@gmail.com", "orderTotal": %s}' % value
            self.assertEqual(self.post_order(body).code, 400, value)

    # --- error response format ---

    def test_errors_are_returned_as_json(self):
        response = self.post_order({"email": "customer01@gmail.com", "orderTotal": -50})

        self.assertIn("application/json", response.headers["Content-Type"])
        self.assertEqual(json.loads(response.body),
                         {"error": "'orderTotal' must be a non-negative number"})

    def test_missing_reward_tiers_returns_500_with_message(self):
        self.db.rewards.docs = []
        response = self.post_order({"email": "customer01@gmail.com", "orderTotal": 100})

        self.assertEqual(response.code, 500)
        self.assertEqual(json.loads(response.body), {"error": "Reward tiers are not configured"})
        self.assertEqual(self.db.customers.docs, [])


if __name__ == "__main__":
    unittest.main()
