from handlers.rewards_handler import RewardsHandler
from handlers.all_customer_reward_handler import AllCustomerRewardHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/allcustomersreward', AllCustomerRewardHandler),
    
]
