from handlers.reward_tiers_handler import GetRewardTiersHandler
from handlers.user_tier_handler import UserTierHandler
from handlers.user_rewards_handler import GetUserRewardsHandler

url_patterns = [
    (r"/", GetRewardTiersHandler),
    (r"/rewards/order", UserTierHandler),
    (r"/rewards/(?:.*)?", GetUserRewardsHandler),
]
