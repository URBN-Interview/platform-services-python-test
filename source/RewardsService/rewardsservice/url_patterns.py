# Importing all of the handlers
from handlers.rewards_handler import *

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/order_data', OrderDatatHandler),
    (r'/find_rewards_data', FindRewardsDatatHandler),
]
