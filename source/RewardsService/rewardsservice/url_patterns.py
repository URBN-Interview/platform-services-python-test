from handlers.customer_rewards_handler import CustomerRewardsHandler
from handlers.rewards_handler import RewardsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomerRewardsHandler),
]
