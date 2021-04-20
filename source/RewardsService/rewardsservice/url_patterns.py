from handlers.rewards_handler import RewardsHandler
from handlers.updateCustomer import updateCustomer

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/uodateCustomer', updateCustomer),
]
