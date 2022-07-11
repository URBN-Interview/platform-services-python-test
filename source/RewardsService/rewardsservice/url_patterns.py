from handlers.rewards_handler import RewardsHandler
from handlers.rewards_handler import RewardCalHandler
from handlers.rewards_handler import RewardDetailHandler
from handlers.rewards_handler import AllDetailHandler
url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/addreward', RewardCalHandler),
    (r'/getReward', RewardDetailHandler),
    (r'/getAllReward', AllDetailHandler)
]
