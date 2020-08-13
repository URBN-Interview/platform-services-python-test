from handlers.rewards_handler import RewardsHandler, CustomerData, CustomerSummary, AllCustomers

#define endpoint settings
url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/info', CustomerData),
    (r'/getone', CustomerSummary),
    (r'/getall', AllCustomers)
]
