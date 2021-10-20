from handlers import *

url_patterns = [
    (r'/', RootHandler),
    (r'/rewards', RewardsHandler),
    (r'/tiers', RewardTiersHandler)
]
