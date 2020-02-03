from handlers.rewards_handler import RewardsHandler
from handlers.all_customers_handler import AllCustomersHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/allcustomers', AllCustomersHandler),
]
