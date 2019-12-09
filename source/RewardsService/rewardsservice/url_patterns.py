from handlers.rewards_handler import RewardsHandler
from handlers.customer_rewards_handler import CustomerRewardsHandler
from handlers.orders_handler import OrdersHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customer-rewards', CustomerRewardsHandler),
    (r'/orders', OrdersHandler),
]
