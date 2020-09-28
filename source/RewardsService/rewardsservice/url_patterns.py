from handlers.rewards_handler import RewardsHandler
from handlers.all_customers_handler import AllCustomersHandler
from handlers.orders_handler import OrdersHandler
from handlers.customers_handler import CustomersHandler


url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomersHandler),
    (r'/customers/all', AllCustomersHandler),
    (r'/orders', OrdersHandler)
]
