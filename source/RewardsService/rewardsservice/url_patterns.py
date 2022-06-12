from handlers.rewards_handler import RewardsHandler
from handlers.customer_reward_handler import CustomerRewardsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomerRewardsHandler),
]
