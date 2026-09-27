from handlers.rewards_handler import RewardsHandler
from tornado.routing import _RuleList


def build_url_patterns(rewards_repo, customer_repo) -> "_RuleList":
    rewards_kwargs = {"repo": rewards_repo}
    customer_kwargs = {"repo": customer_repo}
    
    return [
    (r'/rewards', RewardsHandler, rewards_kwargs),
]
