from handlers.rewards_handler import RewardsHandler 
from handlers.endpoint_handlers import EndPointOne, EndPointTwo, EndPointThree

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/endpoint_one', EndPointOne),
    (r'/endpoint_two', EndPointTwo),
    (r'/endpoint_three', EndPointThree)
]

