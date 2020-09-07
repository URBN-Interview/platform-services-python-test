from handlers.rewards_handler import RewardsHandler, CustomerHandler, OrderHandler, CustomerDataHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/allCustomers', CustomerHandler),
    (r'/order/(.*)', OrderHandler),
    (r'/customer/(.*)', CustomerDataHandler)
]
