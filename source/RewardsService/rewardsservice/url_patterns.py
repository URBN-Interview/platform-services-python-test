from handlers.rewards_handler import RewardsHandler, CalculateRewardsHandler, RetrieveCustomerRewardsHandler, RetrieveAllCustomersRewardsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r"/calculate_rewards", CalculateRewardsHandler),
    (r"/retrieve_rewards/([^/]+)", RetrieveCustomerRewardsHandler),
    (r"/retrieve_all_rewards", RetrieveAllCustomersRewardsHandler),
]
