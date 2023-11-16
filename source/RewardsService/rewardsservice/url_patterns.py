from handlers.rewards_handler import AllRewardsHandler
from handlers.order_data_handler import UserTierHandler

url_patterns = [
    (r"/rewards", AllRewardsHandler),
    (r"/rewards/order", UserTierHandler),
]
