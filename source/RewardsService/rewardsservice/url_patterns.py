from handlers.rewards_handler import RewardsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/rewards/single_customer', RewardsHandler),
    (r'/rewards/all_customers', RewardsHandler),

]
