from handlers.rewards_handler import RewardsHandler
from handlers.customer_order_handler import CustomerOrderHandler, AllCustomersHandler, CustomerHandler




url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/order', CustomerOrderHandler),
    (r'/customer', CustomerHandler),
    (r'/customers', AllCustomersHandler)
]
