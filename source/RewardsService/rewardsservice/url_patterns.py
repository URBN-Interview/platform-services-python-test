from handlers.rewards_handler import RewardsHandler, Init, CustomerData, CustomerSummary, AllCustomers

#define endpoint settings
url_patterns = [
    #test that this works
    (r'/', Init),
    (r'/rewards', RewardsHandler),
    (r'/info', CustomerData),
    (r'/getone', CustomerSummary),
    (r'/getall', AllCustomers)
]
