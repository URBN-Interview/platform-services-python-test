from handlers.rewards_handler import RewardsHandler
from handlers.updateCustomer import updateCustomer
from handlers.displayCustomer import displayCustomer
from handlers.displayAllCustomer import displayAllCustomer

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/updateCustomer', updateCustomer),
    (r'/customer', displayCustomer),
    (r'/customers', displayAllCustomer),
]
