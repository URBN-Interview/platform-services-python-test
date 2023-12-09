from handlers.rewards_handler import RewardsHandler
from handlers.order_handler import OrderHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/order', OrderHandler)
]
