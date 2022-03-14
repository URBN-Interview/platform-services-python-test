from handlers.rewards_handler import RewardsHandler
from handlers.customer_handler import CustomerHandler
from handlers.order_handler import OrderHandler
from handlers.customers_handler import CustomersHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/order', OrderHandler),
    (r'/customer', CustomerHandler),
    (r'/customers', CustomersHandler),
]
