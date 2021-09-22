from handlers.rewards_handler import RewardsHandler
from handlers.rewards_handler import CustomerRewards

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customer/rewards', CustomerRewards),
    (r'/customer/rewards/([^/]*)', CustomerRewards)
]
