from source.RewardsService.rewardsservice.handlers.rewards_handler import RewardsHandler, CustomerRewardHandler, \
    ListCustomerRewardHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/me/rewards', CustomerRewardHandler),
    (r'/rewards/customers', ListCustomerRewardHandler)
]
