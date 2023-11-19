from handlers.rewards_handler import RewardsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/order/rewards', RewardsHandler),
    (r'/user/rewards', RewardsHandler),
    (r'/allcustomers/rewards', RewardsHandler),
]
