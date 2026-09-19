from handlers.customers_handler import CustomerHandler, CustomersHandler
from handlers.orders_handler import OrdersHandler
from handlers.rewards_handler import RewardsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/rewards/orders', OrdersHandler),
    (r'/rewards/customers', CustomersHandler),
    (r'/rewards/customers/([^/]+)', CustomerHandler),
]
