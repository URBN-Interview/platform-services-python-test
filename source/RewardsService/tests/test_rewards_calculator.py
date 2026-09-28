import unittest

from rewardsservice.helpers import rewards_calculator

TIERS = [
    {"tier": "A", "rewardName": "5% off purchase", "points": 100},
    {"tier": "B", "rewardName": "10% off purchase", "points": 200},
    {"tier": "C", "rewardName": "15% off purchase", "points": 300},
]


class TestGetRewardsPointsForPurchase(unittest.TestCase):
    def test_rounds_down_to_whole_points(self):
        self.assertEqual(rewards_calculator.get_rewards_points_for_purchase(100.80), 100)


class TestCustomerRewardsFields(unittest.TestCase):
    def test_below_first_tier(self):
        fields = rewards_calculator.customer_rewards_fields(50, TIERS)
        self.assertIsNone(fields["reward_tier"])
        self.assertEqual(fields["next_reward_tier"], "A")
        self.assertEqual(fields["next_reward_tier_progress"], 0.5)

    def test_exactly_at_tier_threshold(self):
        fields = rewards_calculator.customer_rewards_fields(100, TIERS)
        self.assertEqual(fields["reward_tier"], "A")
        self.assertEqual(fields["next_reward_tier"], "B")
        self.assertEqual(fields["next_reward_tier_progress"], 0.0)

    def test_between_tiers(self):
        fields = rewards_calculator.customer_rewards_fields(150, TIERS)
        self.assertEqual(fields, {
            "reward_tier": "A",
            "reward_tier_name": "5% off purchase",
            "next_reward_tier": "B",
            "next_reward_tier_name": "10% off purchase",
            "next_reward_tier_progress": 0.5,
        })

    def test_top_tier_has_no_next_tier(self):
        fields = rewards_calculator.customer_rewards_fields(350, TIERS)
        self.assertEqual(fields["reward_tier"], "C")
        self.assertIsNone(fields["next_reward_tier"])
        self.assertEqual(fields["next_reward_tier_progress"], 1.0)


if __name__ == "__main__":
    unittest.main()
