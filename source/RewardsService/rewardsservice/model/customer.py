# Customer DB model	
class Customers:	
    def __init__(self, email, orderTotal):	
        self.email = email	
        self.orderTotal = orderTotal	
        self.rewardName = ""	
        self.tier = 0
        self.points = 0.0
        self.nextReward = 0.0	
        self.nextTier = ""	
        self.progress = 0.0	

    def currentReward(self, tier, name, points):	
        self.tier = tier	
        self.rewardName = name	
        self.points = points	

    def newReward(self, tier, name, progress):	
        self.tier = tier	
        self.rewardName = name	
        self.progress = progress