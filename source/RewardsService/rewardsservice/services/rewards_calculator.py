import math


def points_earned_for_order(order_total):
    """1 reward point per whole dollar spent (e.g. $100.80 -> 100 points)."""
    return math.floor(order_total)


def calculate_rewards(total_points, tiers):
    """Compute a customer's reward tier standing from their cumulative points.

    ``tiers`` is the list of reward tier docs (each with ``tier``,
    ``rewardName`` and ``points``); it does not need to be pre-sorted.

    Once a customer reaches the top tier there is nothing left to earn, so
    total points are capped at the top tier's threshold and there is no
    "next" tier.
    """
    sorted_tiers = sorted(tiers, key=lambda t: t["points"])

    if not sorted_tiers:
        return {
            "rewardPoints": total_points,
            "rewardTier": None,
            "rewardTierName": None,
            "nextRewardTier": None,
            "nextRewardTierName": None,
            "nextRewardTierProgress": None,
        }

    max_points = sorted_tiers[-1]["points"]
    total_points = min(total_points, max_points)

    current_tier = None
    next_tier = None
    for tier in sorted_tiers:
        if tier["points"] <= total_points:
            current_tier = tier
        elif next_tier is None:
            next_tier = tier

    return {
        "rewardPoints": total_points,
        "rewardTier": current_tier["tier"] if current_tier else None,
        "rewardTierName": current_tier["rewardName"] if current_tier else None,
        "nextRewardTier": next_tier["tier"] if next_tier else None,
        "nextRewardTierName": next_tier["rewardName"] if next_tier else None,
        "nextRewardTierProgress": (
            round(total_points / next_tier["points"], 4) if next_tier else None
        ),
    }
