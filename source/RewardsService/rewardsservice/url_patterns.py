from handlers.rewards_handler import RewardsHandler, CustomersHandler, CustomerHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomersHandler),
    (r'/customers/([^/]+)', CustomerHandler)
]
