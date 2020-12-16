from handlers.rewards_handler import RewardsHandler
from handlers.rewards_update import RewardsUpdate

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/endpoint1', RewardsUpdate),
]
