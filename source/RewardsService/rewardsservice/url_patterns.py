from handlers.rewards_handler import AllRewardsHandler
from handlers.order_data_handler import OrderDataHandler

url_patterns = [
    (r"/rewards", AllRewardsHandler),
    (r"/rewards/order", OrderDataHandler),
]
