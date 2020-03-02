from handlers.rewards_handler import RewardsHandler
from handlers.all_customers_handler import AllCustomersHandler
from handlers.customer_handler import CustomerHandler
from handlers.order_handler import OrderHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', AllCustomersHandler),
    (r'/customer', CustomerHandler),
    (r'/order', OrderHandler)
]
