from handlers.rewards_handler import RewardsHandler
from handlers.customer_order_rewards_handler import CustomerOrderRewardsHandler
from handlers.customer_rewards_handler import CustomerRewardsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customer_order_rewards', CustomerOrderRewardsHandler),
    (r'/customer_rewards', CustomerRewardsHandler)
]
