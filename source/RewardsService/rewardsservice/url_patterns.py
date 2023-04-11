from handlers.rewards_handler import RewardsHandler
from handlers.order_handler import OrderHandler
from handlers.customer_rewards_data_handler import RewardsDataHandler
from handlers.customers_handler import CustomersHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/addRewards', OrderHandler),
    (r'/getCustomerRewards', RewardsDataHandler),
    (r'/getCustomers', CustomersHandler),
]
