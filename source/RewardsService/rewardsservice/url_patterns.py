from handlers.order_handler import OrderHandler
from handlers.customer_handler import CustomerHandler
from handlers.customers_rewards_handler import (
    CustomersRewardsHandler,
)
from handlers.rewards_handler import RewardsHandler

url_patterns = [
    (r"/orders", OrderHandler),
    (r"/customers", CustomersRewardsHandler),
    (r"/customers/([^/]+)", CustomerHandler),
    (r"/rewards", RewardsHandler),
]
