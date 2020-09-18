from handlers.rewards_handler import RewardsHandler
from handlers.users_and_points_handler import UsersAndPointsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', UsersAndPointsHandler),
]
