from handlers.rewards_handler import RewardsHandler, RewardPointsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/rewardpoint', RewardPointsHandler,)
]
