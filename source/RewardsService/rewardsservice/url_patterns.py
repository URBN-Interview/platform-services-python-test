from handlers.rewards_handler import RewardsHandler
from handlers.orders_handler import OrdersHandler
from handlers.customer_handler import SingleCustomerHandler, AllCustomerHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/order', OrdersHandler),
    (r'/customer-rewards', SingleCustomerHandler),
    (r'/all-customer-rewards', AllCustomerHandler),
]
