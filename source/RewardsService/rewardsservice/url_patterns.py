# Import handlers
from handlers.rewards_handler import RewardsHandler, CustomerRewardsHandler

# Define URL patterns
url_patterns = [
    (r'/rewards', RewardsHandler),                # Associates '/rewards' URL with RewardsHandler class
    (r'/customers', CustomerRewardsHandler)       # Associates '/customers' URL with CustomerRewardsHandler class
]
