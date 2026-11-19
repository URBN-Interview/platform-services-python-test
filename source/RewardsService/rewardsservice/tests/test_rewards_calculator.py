import unittest
from decimal import Decimal

from rewards_calculator import (
    ValidationError,
    calculate_rewards,
    normalize_email,
    parse_order_total,
    points_for_order,
)

TIERS = [
    {"tier": chr(ord("A") + i), "rewardName": "{}% off purchase".format(5 * (i + 1)), "points": 100 * (i + 1)}
    for i in range(10)
]


class PointsForOrderTest(unittest.TestCase):

    def test_one_point_per_whole_dollar(self):
        self.assertEqual(points_for_order(100.80), 100)
        self.assertEqual(points_for_order("250.99"), 250)
        self.assertEqual(points_for_order(0.99), 0)
        self.assertEqual(points_for_order(42), 42)

    def test_rejects_invalid_totals(self):
        for bad in (-1, "-0.01", "abc", "", None, True, [], {}, "nan", "inf"):
            with self.subTest(order_total=bad):
                with self.assertRaises(ValidationError):
                    points_for_order(bad)

    def test_parse_order_total_returns_decimal(self):
        self.assertEqual(parse_order_total("100.80"), Decimal("100.80"))


class NormalizeEmailTest(unittest.TestCase):

    def test_trims_and_lowercases(self):
        self.assertEqual(normalize_email("  Customer01@Gmail.com "), "customer01@gmail.com")

    def test_rejects_invalid_emails(self):
        for bad in ("", "no-at-sign", "a@b", "a b@c.com", None, 123, "a@" + "b" * 260 + ".com"):
            with self.subTest(email=bad):
                with self.assertRaises(ValidationError):
                    normalize_email(bad)


class CalculateRewardsTest(unittest.TestCase):

    def test_readme_example(self):
        self.assertEqual(calculate_rewards("customer01@gmail.com", 100, TIERS), {
            "email": "customer01@gmail.com",
            "points": 100,
            "tier": "A",
            "tierName": "5% off purchase",
            "nextTier": "B",
            "nextTierName": "10% off purchase",
            "nextTierProgress": 0.5,
        })

    def test_below_first_tier(self):
        result = calculate_rewards("c@x.com", 50, TIERS)
        self.assertIsNone(result["tier"])
        self.assertIsNone(result["tierName"])
        self.assertEqual(result["nextTier"], "A")
        self.assertEqual(result["nextTierProgress"], 0.5)

    def test_between_tiers(self):
        result = calculate_rewards("c@x.com", 450, TIERS)
        self.assertEqual(result["tier"], "D")
        self.assertEqual(result["nextTier"], "E")
        self.assertEqual(result["nextTierProgress"], 0.9)

    def test_exact_tier_boundary(self):
        result = calculate_rewards("c@x.com", 200, TIERS)
        self.assertEqual(result["tier"], "B")
        self.assertEqual(result["nextTier"], "C")

    def test_top_tier_caps_points(self):
        result = calculate_rewards("c@x.com", 1500, TIERS)
        self.assertEqual(result["points"], 1000)
        self.assertEqual(result["tier"], "J")
        self.assertEqual(result["tierName"], "50% off purchase")
        self.assertIsNone(result["nextTier"])
        self.assertIsNone(result["nextTierName"])
        self.assertEqual(result["nextTierProgress"], 1.0)

    def test_tiers_order_does_not_matter(self):
        self.assertEqual(
            calculate_rewards("c@x.com", 333, list(reversed(TIERS))),
            calculate_rewards("c@x.com", 333, TIERS),
        )


if __name__ == "__main__":
    unittest.main()
