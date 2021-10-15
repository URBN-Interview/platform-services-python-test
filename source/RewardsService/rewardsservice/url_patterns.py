from handlers.rewards_handler import RewardsHandler
from handlers.customer_order_rewards_handler import CustomerOrderRewardsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customer_order_rewards', CustomerOrderRewardsHandler)
]
