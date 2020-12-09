from handlers.rewards_handler import RewardsHandler
from handlers.rewards_handler import CustomerData

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/data', CustomerData),
]
