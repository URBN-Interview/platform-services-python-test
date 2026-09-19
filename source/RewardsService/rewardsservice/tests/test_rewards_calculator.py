import unittest

from services.rewards_calculator import calculate_rewards, points_earned_for_order

TIERS = [
    {"tier": "A", "rewardName": "5% off purchase", "points": 100},
    {"tier": "B", "rewardName": "10% off purchase", "points": 200},
    {"tier": "C", "rewardName": "15% off purchase", "points": 300},
    {"tier": "J", "rewardName": "50% off purchase", "points": 1000},
]


class PointsEarnedForOrderTests(unittest.TestCase):

    def test_floors_to_whole_dollars(self):
        self.assertEqual(points_earned_for_order(100.80), 100)

    def test_handles_whole_dollar_amounts(self):
        self.assertEqual(points_earned_for_order(100.0), 100)

    def test_amount_under_a_dollar_earns_zero(self):
        self.assertEqual(points_earned_for_order(0.50), 0)


class CalculateRewardsTests(unittest.TestCase):

    def test_below_first_tier(self):
        result = calculate_rewards(50, TIERS)
        self.assertIsNone(result["rewardTier"])
        self.assertIsNone(result["rewardTierName"])
        self.assertEqual(result["nextRewardTier"], "A")
        self.assertEqual(result["nextRewardTierName"], "5% off purchase")
        self.assertEqual(result["nextRewardTierProgress"], 0.5)

    def test_exactly_on_a_tier_boundary_matches_dashboard_mock(self):
        # customer01@gmail.com in the dashboard mock: 100 points, tier A,
        # next tier B, 50% progress.
        result = calculate_rewards(100, TIERS)
        self.assertEqual(result["rewardTier"], "A")
        self.assertEqual(result["rewardTierName"], "5% off purchase")
        self.assertEqual(result["nextRewardTier"], "B")
        self.assertEqual(result["nextRewardTierName"], "10% off purchase")
        self.assertEqual(result["nextRewardTierProgress"], 0.5)

    def test_mid_tier_progress(self):
        result = calculate_rewards(150, TIERS)
        self.assertEqual(result["rewardTier"], "A")
        self.assertEqual(result["nextRewardTier"], "B")
        self.assertEqual(result["nextRewardTierProgress"], 0.75)

    def test_at_top_tier_has_no_next_tier(self):
        result = calculate_rewards(1000, TIERS)
        self.assertEqual(result["rewardTier"], "J")
        self.assertEqual(result["rewardTierName"], "50% off purchase")
        self.assertIsNone(result["nextRewardTier"])
        self.assertIsNone(result["nextRewardTierName"])
        self.assertIsNone(result["nextRewardTierProgress"])

    def test_points_are_capped_at_top_tier(self):
        result = calculate_rewards(5000, TIERS)
        self.assertEqual(result["rewardPoints"], 1000)
        self.assertEqual(result["rewardTier"], "J")
        self.assertIsNone(result["nextRewardTier"])

    def test_no_tiers_configured(self):
        result = calculate_rewards(100, [])
        self.assertEqual(result["rewardPoints"], 100)
        self.assertIsNone(result["rewardTier"])
        self.assertIsNone(result["nextRewardTier"])

    def test_tiers_do_not_need_to_be_pre_sorted(self):
        shuffled = [TIERS[2], TIERS[0], TIERS[3], TIERS[1]]
        result = calculate_rewards(150, shuffled)
        self.assertEqual(result["rewardTier"], "A")
        self.assertEqual(result["nextRewardTier"], "B")


if __name__ == "__main__":
    unittest.main()
