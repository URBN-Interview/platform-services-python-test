from handlers.rewards_handler import RewardsHandler
from handlers.endpoint1 import Endpoint1
from handlers.endpoint3 import Endpoint3
# from handlers.endpoint2 import Endpoint2

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/endpoint1', Endpoint1),
    # (r'/endpoint2', Endpoint2),
    (r'/endpoint3', Endpoint3)
]
