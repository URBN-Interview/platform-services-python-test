from handlers.rewards_handler import RewardsHandler
from handlers.rewards_update import RewardsUpdate
from handlers.user_rewards import UserRewards

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/endpoint1', RewardsUpdate),
    (r'/endpoint2', UserRewards),
]
