from handlers.rewards_handler import GetRewardTiersHandler
from handlers.order_data_handler import UserTierHandler

url_patterns = [
    (r"/", GetRewardTiersHandler),
    (r"/rewards/order", UserTierHandler),
    ("r/rewards/(?:^\S+@\S+\.\S+$)?", GetUserRewardsHandler),
]
