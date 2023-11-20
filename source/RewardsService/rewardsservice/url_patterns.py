from handlers.rewards_handler import RewardsHandler
from handlers.rewards_status_handler import RewardsStatusHandler
from handlers.rewards_data_handler import RewardsDataHandler
from handlers.customer_rewards_data_handler import CustomerRewardsDataHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/get-customers', RewardsDataHandler),
]
