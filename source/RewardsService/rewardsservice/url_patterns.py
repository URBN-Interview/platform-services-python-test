from handlers.rewards_handler import RewardsHandler
from handlers.endpoint1 import Endpoint1

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/endpoint1', Endpoint1)
]
