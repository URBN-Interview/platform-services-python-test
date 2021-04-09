from handlers.rewards_handler import RewardsHandler
from handlers.user_handler import UserHandler
from handlers.user_retrieve_handler import UserRetrieveHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/user_info', UserHandler),
    (r'/retrieve_user_info', UserRetrieveHandler)
]
