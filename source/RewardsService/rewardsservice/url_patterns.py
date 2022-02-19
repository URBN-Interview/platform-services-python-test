from handlers.rewards_handler import RewardsHandler
from handlers.customer_handler import CustomerHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomerHandler)
]
