from handlers.rewards_handler import RewardsHandler
from handlers.customers_handler import CustomersHandler
from handlers.all_customers_handler import AllCustomersHandler
from handlers.orders_handler import OrdersHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomersHandler),
    (r'/allcustomers', AllCustomersHandler),
    (r'/orders', OrdersHandler),
]
