from handlers.rewards_handler import RewardsHandler, InsertHandler, CustomerHandler, AllHandler, ClearHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/insert', InsertHandler),
    (r'/find', CustomerHandler),
    (r'/all', AllHandler),
    (r'/clear', ClearHandler)
]
