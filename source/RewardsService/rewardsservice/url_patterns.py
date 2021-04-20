from handlers.rewards_handler import RewardsHandler
from handlers.rewards_handler import MyFormHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/form', MyFormHandler),
    (r'/response', MyFormHandler)
]
