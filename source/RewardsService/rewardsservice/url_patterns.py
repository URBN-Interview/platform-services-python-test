from handlers.rewards_handler import RewardsHandler
from handlers.rewards_handler import CustomerData
from handlers.rewards_handler import ReturnRewards
from handlers.rewards_handler import RewardMembers

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/postData', CustomerData),
    (r'/getRewards', ReturnRewards),
    (r'/rewardMembers', RewardMembers)
]
