from handlers.rewards_handler import RewardsHandler
from handlers.order_data_handler import OrderDataHandler

url_patterns = [
    (r"/rewards", RewardsHandler),
    (r"/rewards/order", OrderDataHandler),
]
