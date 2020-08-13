from handlers.rewards_handler import RewardsHandler
from handlers.set_customer_handler import SetCustomerHandler
from handlers.get_customer_handler import GetCustomer
from handlers.delete_customer_handler import DeleteCustomer
from handlers.get_all_customer_handler import AllCustomer

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/set', SetCustomerHandler),
    (r'/get', GetCustomer),
    (r'/del', DeleteCustomer),
    (r'/all', AllCustomer),
]
