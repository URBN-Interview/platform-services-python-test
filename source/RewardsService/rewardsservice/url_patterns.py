from handlers.rewards_handler import RewardsHandler
from handlers.orders_handler import OrdersHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/orders', OrdersHandler),
]
