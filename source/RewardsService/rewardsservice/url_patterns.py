from handlers.rewards_handler import RewardsHandler, Init

#define endpoint settings
url_patterns = [
    #test that this works
    (r'/', Init),
    (r'/rewards', RewardsHandler),
]
