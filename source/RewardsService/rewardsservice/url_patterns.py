from handlers.rewards_handler import RewardsHandler
from handlers.index_handler import IndexHandler
from handlers.customer_handler import CustomerHandler
from handlers.customers_handler import CustomersHandler
from handlers.processOrder_handler import ProcessOrderHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/', IndexHandler),
    (r'/customer', CustomerHandler),
    (r'/customers', CustomersHandler),
    (r'/processOrder/', ProcessOrderHandler)
]
