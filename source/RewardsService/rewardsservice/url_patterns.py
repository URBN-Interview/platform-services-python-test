from handlers.rewards_handler import RewardsHandler
from handlers.customer_rewards_handler import SingleCustomerHandler
from handlers.customer_rewards_handler import CustomerRewardsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customer-rewards/(.+)', SingleCustomerHandler),
    (r'/customer-rewards/', CustomerRewardsHandler)
]
