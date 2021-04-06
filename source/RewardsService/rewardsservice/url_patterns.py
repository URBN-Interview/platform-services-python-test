from handlers.rewards_handler import RewardsHandler
from handlers.customer_order import CustomerOrder

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomerOrder)
]
