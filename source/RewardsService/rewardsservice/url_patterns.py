from handlers.rewards_handler import RewardsHandler
from handlers.order_handler import OrderHandler
from handlers.customer_handler import CustomerHandler 
from handlers.all_customer_handler import AllCustomerHandler 

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/orders', OrderHandler),
    (r'/customer', CustomerHandler),
    (r'/customers', AllCustomerHandler),
]
