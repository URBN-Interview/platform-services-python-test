from handlers.main_handler import MainHandler
from handlers.rewards_handler import RewardsHandler
from handlers.customer_handler import CustomerHandler	
from handlers.customers_handler import CustomersHandler	
from handlers.order_handler import OrderHandler


url_patterns = [
    (r'/', MainHandler),
    (r'/rewards', RewardsHandler),
    (r'/orders', OrderHandler),	
    (r'/customer', CustomerHandler),	
    (r'/customers', CustomersHandler),
]
