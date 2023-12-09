from handlers.rewards_handler import RewardsHandler, OrderHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/order', OrderHandler)
]
