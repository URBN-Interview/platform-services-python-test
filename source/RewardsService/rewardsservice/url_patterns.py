from handlers.rewards_handler import RewardsHandler
from handlers.rewards_data_handler import RewardsDataHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/rewards_data', RewardsDataHandler),
]
