from handlers.rewards_handler import RewardsHandler
from handlers.customer_data_handler import CustomerDataHandler, CustomersDataHandler
from tornado.routing import _RuleList


def build_url_patterns(rewards_repo, customer_repo) -> "_RuleList":
    rewards_kwargs = {"repo": rewards_repo}
    customers_kwargs = {"customer_repo": customer_repo}
    customer_kwargs = {"customer_repo": customer_repo, "rewards_repo": rewards_repo}
    
    return [
    (r'/rewards', RewardsHandler, rewards_kwargs),
    (r'/customers', CustomersDataHandler, customers_kwargs),
    (r'/customer', CustomerDataHandler, customer_kwargs),
    (r'/customer/([^/]+)', CustomerDataHandler, customer_kwargs)
]
