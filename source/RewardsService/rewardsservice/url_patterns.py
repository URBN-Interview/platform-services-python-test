from handlers.rewards_handler import RewardsHandler
from rewardsservice.handlers.rewards_handler import EmailHandler, OrderHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/rewards/users', EmailHandler),
    (r'/rewards/order', OrderHandler),
]
