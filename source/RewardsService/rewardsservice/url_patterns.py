from handlers.rewards_handler import RewardsHandler
from handlers.index_handler import IndexHandler
from handlers.customer_handler import CustomerHandler
from handlers.customers_handler import CustomersHandler
from handlers.processOrder_handler import ProcessOrderHandler

url_patterns = [
    ('/rewards', RewardsHandler),
    ('/', IndexHandler),
    ('/customer', CustomerHandler),
    ('/customers', CustomersHandler),
    ('/processOrder', ProcessOrderHandler),
]
