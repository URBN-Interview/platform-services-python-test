import pytest

from rewardsservice.handlers.post_calculate_rewards_handler import get_tier

# updated to test different point intervals
REWARDS = [{"rewardName": "5% off purchase", "points": 100, "tier": "A"},
           {"rewardName": "10% off purchase", "points": 200, "tier": "B"},
           {"rewardName": "15% off purchase", "points": 300, "tier": "C"},
           {"rewardName": "20% off purchase", "points": 400, "tier": "D"},
           {"rewardName": "25% off purchase", "points": 550, "tier": "E"},
           {"rewardName": "30% off purchase", "points": 600, "tier": "F"},
           {"rewardName": "35% off purchase", "points": 730, "tier": "G"},
           {"rewardName": "40% off purchase", "points": 800, "tier": "H"},
           {"rewardName": "45% off purchase", "points": 900, "tier": "I"},
           {"rewardName": "50% off purchase", "points": 1000, "tier": "J"}]


@pytest.mark.parametrize("points,rewards,expected", [
    (50, REWARDS, {"tier": "",
                   "reward_name": "",
                   "next_tier": "A",
                   "next_tier_name": "5% off purchase",
                   "next_tier_progress": "50.0 %"}),
    (1500, REWARDS, {"tier": "J",
                     "reward_name": "50% off purchase",
                     "next_tier": "",
                     "next_tier_name": "",
                     "next_tier_progress": ""})
])
def test_get_tier_points_outside_range(points, rewards, expected):
    assert get_tier(points, rewards) == expected


@pytest.mark.parametrize("points,rewards,expected", [
    (100, REWARDS, {"tier": "A",
                    "reward_name": "5% off purchase",
                    "next_tier": "B",
                    "next_tier_name": "10% off purchase",
                    "next_tier_progress": "50.0 %"}),
    (150, REWARDS, {"tier": "A",
                    "reward_name": "5% off purchase",
                    "next_tier": "B",
                    "next_tier_name": "10% off purchase",
                    "next_tier_progress": "75.0 %"}),
    (500, REWARDS, {"tier": "D",
                    "reward_name": "20% off purchase",
                    "next_tier": "E",
                    "next_tier_name": "25% off purchase",
                    "next_tier_progress": "90.91 %"}),
    (1000, REWARDS, {"tier": "J",
                     "reward_name": "50% off purchase",
                     "next_tier": "",
                     "next_tier_name": "",
                     "next_tier_progress": ""})
])
def test_get_tier_returns_correct_tier_data(points, rewards, expected):
    assert get_tier(points, rewards) == expected
