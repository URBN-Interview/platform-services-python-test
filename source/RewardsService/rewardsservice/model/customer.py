class Customer:
    def __init__(self, email, orderTotal):
        self.email = email
        self.orderTotal = orderTotal
        self.rewardTier = None
        self.rewardName = None
        self.nextRewardTier = None
        self.nextRewardName = None
        self.tierProgress = 0.0

    def setReward(self, rewardTier, rewardName):
        self.rewardTier = rewardTier
        self.rewardName = rewardName
    
    def setNextReward(self, nextRewardTier, nextRewardName):
        self.nextRewardTier = nextRewardTier
        self.nextRewardName = nextRewardName

