from handlers.rewards_handler import RewardsHandler
from handlers.orders_handler import OrdersHandler
from handlers.customers_handler import CustomerHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/orders', OrdersHandler),
    (r'/customers/([^/]+)', CustomerHandler),
]

