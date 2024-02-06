from handlers.rewards_handler import RewardsHandler
from handlers.orders_handlers import OrdersHandler, OrderHandler

url_patterns = [
    (r"/rewards", RewardsHandler),
    (r"/orders", OrdersHandler),
    (r"/order", OrderHandler),
]
