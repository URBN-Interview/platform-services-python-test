from handlers.rewards_handler import RewardsHandler
from handlers.customer_handler import CustomerHandler
from handlers.admin_handler import AdminHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomerHandler),
    (r'/admin', AdminHandler)
]
