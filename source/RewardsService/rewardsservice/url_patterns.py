from rewardsservice.handlers.rewards_handler import RewardsHandler
from rewardsservice.handlers.post_calculate_rewards_handler import CalculateRewardsHandler
from rewardsservice.handlers.get_customer_rewards_handler import CustomerRewardsHandler
from rewardsservice.handlers.get_all_customer_data_handler import CustomerDataHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/calculate_rewards', CalculateRewardsHandler),
    (r'/customer_rewards', CustomerRewardsHandler),
    (r'/customer_data', CustomerDataHandler)
]
