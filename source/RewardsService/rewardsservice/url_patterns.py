from handlers.rewards_handler import RewardsHandler
from handlers.customers_handler import CustomersHandler
from handlers.customer_handler import CustomerHandler
from db import Database

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomersHandler, dict(db=Database())),
    (r'/customer', CustomerHandler, dict(db=Database())),

]
