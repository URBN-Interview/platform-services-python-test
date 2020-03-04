class Customer:
    def __init__(self, email, orderTotal):
        self.email = email
        self.orderTotal = orderTotal
        self.rewardTier = None
        self.rewardName = None
        self.rewardPoints = None
        self.nextRewardTier = None
        self.nextRewardName = None
        self.tierProgress = 0.0

    def setReward(self, tier, name, points):
        self.rewardTier = tier
        self.rewardName = name
        self.rewardPoints = points
    
    def setNextReward(self, tier, name):
        self.nextRewardTier = tier
        self.nextRewardName = name

