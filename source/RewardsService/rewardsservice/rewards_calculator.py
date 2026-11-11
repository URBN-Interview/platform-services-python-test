import math
from decimal import Decimal


def points_for_order(order_total) -> int:
    """Convert an order total to reward points: 1 point per whole dollar ($100.80 -> 100)."""
    # Decimal(str(...)) avoids float surprises like 0.29 being stored as 0.28999...
    return math.floor(Decimal(str(order_total)))


def calculate_rewards(points: int, tiers: list) -> dict:
    """Work out a customer's reward tier data from their total points.

    points: the customer's total reward points
    tiers:  list of tier dicts from the rewards collection,
            e.g. [{"tier": "A", "rewardName": "5% off purchase", "points": 100}, ...]

    Progress is measured within the current band:
    (points - current tier threshold) / (next tier threshold - current tier threshold).
    Customers below the first tier have no tier (None); customers at the top tier
    have no next tier and no progress (None).
    """
    #    sorted() returns a new list, so the caller's list is left untouched.
    sorted_tiers = sorted(tiers, key=lambda tier: tier["points"])

    #    cap customers points at top tier's threshold
    top_tier = sorted_tiers[-1]
    points = min(points, top_tier["points"])

    current_tier = None
    next_tier = None
    for tier in sorted_tiers:
        if tier["points"] <= points:
            current_tier = tier
        else:
            next_tier = tier
            break

    if next_tier is None:
        progress = None
    else:
        start = current_tier["points"] if current_tier else 0
        progress = round((points - start) / (next_tier["points"] - start), 2)

    return {
        "rewardPoints": points,
        "rewardTier": current_tier["tier"] if current_tier else None,
        "rewardTierName": current_tier["rewardName"] if current_tier else None,
        "nextRewardTier": next_tier["tier"] if next_tier else None,
        "nextRewardTierName": next_tier["rewardName"] if next_tier else None,
        "nextRewardTierProgress": progress,
    }
