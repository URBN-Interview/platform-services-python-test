from handlers.rewards_handler import RewardsHandler
from handlers.customer_order_data_handler import CustomerOrderDataHandler
from handlers.customer_rewards_handler import CustomerRewardsHandler, SingleCustomerRewardsDataHandler


url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customerOrderData', CustomerOrderDataHandler),
    (r'/customerRewardsData', CustomerRewardsHandler),
    (r'/singleCustomerRewardsData', SingleCustomerRewardsDataHandler)
]
