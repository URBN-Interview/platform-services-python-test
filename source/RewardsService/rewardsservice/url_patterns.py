from handlers.rewards_handler import RewardsHandler
from handlers.customer_handler import CustomersHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomerHandler)
]
