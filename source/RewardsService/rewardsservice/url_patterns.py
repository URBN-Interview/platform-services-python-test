from handlers.rewards_handler import RewardsHandler
from handlers.all_customer_reward_handler import AllCustomerRewardHandler
from handlers.get_customer_reward_handler import GetCustomerRewardHandler
from handlers.customer_order_handler import CustomerOrderHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customerorder', CustomerOrderHandler), # endpoint1
    (r'/getcustomerreward', GetCustomerRewardHandler), # endpoint2
    (r'/allcustomersreward', AllCustomerRewardHandler), # endpoint3
]
