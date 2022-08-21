from handlers.rewards_handler import RewardsHandler
from handlers.users_handler import UsersHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/users', UsersHandler),
]
