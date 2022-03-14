class Customer:
    def __init__(self, email,rewardPoints):
        self.email = email
        self.rewardPoints = rewardPoints
        self.tierProgress = 0.0

    def setReward(self, tier, name, points):
        self.rewardTier = tier
        self.rewardName = name
        self.rewardPoints = points
    
    def setNextReward(self, tier, name):
        self.nextRewardTier = tier
        self.nextRewardName = name

