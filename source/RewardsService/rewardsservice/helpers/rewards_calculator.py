import math

def progress_to_next_tier(current_points, current_tier_threshold, next_tier_threshold):
    tier_gap = next_tier_threshold - current_tier_threshold
    return round((current_points - current_tier_threshold) / tier_gap, 2)

def customer_rewards_fields(points, tiers):
    current_tier = None
    next_tier = None

    for tier in tiers:
        if tier["points"] <= points:
            current_tier = tier
        elif next_tier is None:
            next_tier = tier

    if not next_tier:
        progress = 1.0
    else:
        progress = progress_to_next_tier(points, current_tier["points"] if current_tier else 0, next_tier["points"])

    return {
        "reward_tier": current_tier["tier"] if current_tier else None,
        "reward_tier_name": current_tier["rewardName"] if current_tier else None,
        "next_reward_tier": next_tier["tier"] if next_tier else None,
        "next_reward_tier_name": next_tier["rewardName"] if next_tier else None,
        "next_reward_tier_progress": progress,
    }
   
def get_rewards_points_for_purchase(order_total):
    # customers get 1 point per dollar spent, rounded down
    # use math.floor so an order of $150.45 is 150 points
    points_per_dollar = 1    
    return math.floor(order_total * points_per_dollar)

