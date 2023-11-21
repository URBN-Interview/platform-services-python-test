from handlers.rewards_handler import RewardsHandler
from handlers.add_order_handler import AddOrderHandler
from handlers.rewards_data_handler import RewardsDataHandler
from handlers.customer_rewards_data_handler import CustomerRewardsDataHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/add-order', AddOrderHandler),
    (r'/get-customers', RewardsDataHandler),
    (r'/get-customer-data', CustomerRewardsDataHandler)
]
