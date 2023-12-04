from handlers.rewards_handler import RewardsHandler, CustomerListHandler, CustomerHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomerListHandler),
    (r'/customers/([^/]+)', CustomerHandler)
]
