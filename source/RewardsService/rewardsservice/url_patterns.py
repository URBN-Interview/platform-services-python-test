from handlers.rewards_handler import RewardsHandler
from handlers.customers_handler import CustomersHandler
from handlers.single_customer_handler import SingleCustomerHandler


url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomersHandler),
    (r'/customers/.*', SingleCustomerHandler),
]
