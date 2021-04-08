from handlers.rewards_handler import RewardsHandler
from handlers.user_handler import UserHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/user_info', UserHandler)
]
