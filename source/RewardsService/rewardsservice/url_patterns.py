from handlers.rewards_handler import RewardsHandler, CustomersHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomersHandler),
]
