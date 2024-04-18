from handlers.rewards_handler import (
    RewardsHandler,
    OrderDataHandler,
    CusotmerRewardDataHandler,
    AllCusotmerRewardDataHandler
)

url_patterns = [
    (r"/rewards", RewardsHandler),
    (r"/orderdata", OrderDataHandler),
    (r"/customerreward", CusotmerRewardDataHandler),
    (r"/allcustomerreward", AllCusotmerRewardDataHandler),
]
