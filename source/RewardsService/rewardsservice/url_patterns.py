from handlers.rewards_handler import RewardsHandler
from handlers.users_and_points_handler import UsersAndPointsHandler
from handlers.get_customer_handler import GetCustomerHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', UsersAndPointsHandler),
    (r'/customer', GetCustomerHandler),
]
