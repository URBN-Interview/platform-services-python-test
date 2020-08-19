from handlers.rewards_handler import RewardsHandler
from handlers.customers_handler import CustomersHandler
from handlers.customer_rewards_handler import CustomerRewardsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomersHandler),
    (r'/customerrewards', CustomerRewardsHandler),
]
