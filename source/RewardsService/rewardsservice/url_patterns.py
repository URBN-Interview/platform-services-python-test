from handlers.rewards_handler import RewardsHandler
from handlers.order_handler import OrderHandler
from handlers.customer_handler import CustomerHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/order', OrderHandler),
    (r'/customer', CustomerHandler)
]
