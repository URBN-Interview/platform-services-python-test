import json 
from math import floor

class RewardCalculators:
    TIER_A = "A"
    TIER_B = "B"
    TIER_C = "C"
    TIER_D = "D"
    TIER_E = "E"
    TIER_F = "F"
    TIER_G = "G"
    TIER_H = "H"
    TIER_I = "I"
    TIER_J = "J"
    NO_TIER = "No Tier"

    TIER_A_NAME = "5% off purchase"
    TIER_B_NAME = "10% off purchase"
    TIER_C_NAME = "15% off purchase"
    TIER_D_NAME = "20% off purchase"
    TIER_E_NAME = "25% off purchase"
    TIER_F_NAME = "30% off purchase"
    TIER_G_NAME = "35% off purchase"
    TIER_H_NAME = "40% off purchase"
    TIER_I_NAME = "45% off purchase"
    TIER_J_NAME = "50% off purchase"
    NO_TIER_NAME = "No Tier"

    TIER_MAP = {
        
        TIER_A: TIER_A_NAME,
        TIER_B: TIER_B_NAME,
        TIER_C: TIER_C_NAME,
        TIER_D: TIER_D_NAME,
        TIER_E: TIER_E_NAME,
        TIER_F: TIER_F_NAME,
        TIER_G: TIER_G_NAME,
        TIER_H: TIER_H_NAME,
        TIER_I: TIER_I_NAME,
        TIER_J: TIER_J_NAME,
        NO_TIER: NO_TIER_NAME

    
    
    }


    def calculateRewardPoints(self, order_total, current_reward_points):
        reward_points = current_reward_points + floor(order_total)
        return reward_points


    def calculateRewardTier(self, reward_points):
        if reward_points < 100:
            return self.NO_TIER

        if reward_points >= 100 and reward_points < 200:
            return self.TIER_A
        
        if reward_points >= 200 and reward_points < 300:
            return self.TIER_B

        if reward_points >= 300 and reward_points < 400:
            return self.TIER_C

        if reward_points >= 400 and reward_points < 500:
            return self.TIER_D

        if reward_points >= 500 and reward_points < 600:
            return self.TIER_E

        if reward_points >= 600 and reward_points < 700:
            return self.TIER_F
        
        if reward_points >= 700 and reward_points < 800:
            return self.TIER_G

        if reward_points >= 800 and reward_points < 900:
            return self.TIER_H
        
        if reward_points >= 900 and reward_points < 1000:
            return self.TIER_I
        
        if reward_points >= 1000:
            return self.TIER_J

    
    def generateRewardTierName(self, reward_tier):
        if reward_tier == self.NO_TIER:
            return self.NO_TIER_NAME

        if reward_tier == self.TIER_A:
            return self.TIER_A_NAME

        if reward_tier == self.TIER_B:
            return self.TIER_B_NAME

        if reward_tier == self.TIER_C:
            return self.TIER_C_NAME
            
        if reward_tier == self.TIER_D:
            return self.TIER_D_NAME

        if reward_tier == self.TIER_E:
            return self.TIER_E_NAME

        if reward_tier == self.TIER_F:
            return self.TIER_F_NAME
    
        if reward_tier == self.TIER_G:
            return self.TIER_G_NAME
        
        if reward_tier == self.TIER_H:
            return self.TIER_H_NAME

        if reward_tier == self.TIER_I:
            return self.TIER_I_NAME
        
        if reward_tier == self.TIER_J:
            return self.TIER_J_NAME
    
    def calculateNextTierAndNextTierName(self, reward_tier):
        if reward_tier == self.NO_TIER:
            return [self.TIER_A, self.TIER_A_NAME]

        if reward_tier == self.TIER_A:
            return [self.TIER_B, self.TIER_B_NAME]

        if reward_tier == self.TIER_B:
            return [self.TIER_C, self.TIER_C_NAME]

        if reward_tier == self.TIER_C:
            return [self.TIER_D, self.TIER_D_NAME]
            
        if reward_tier == self.TIER_D:
            return [self.TIER_E, self.TIER_E_NAME]

        if reward_tier == self.TIER_E:
            return [self.TIER_F, self.TIER_F_NAME]

        if reward_tier == self.TIER_F:
            return [self.TIER_G, self.TIER_G_NAME]
    
        if reward_tier == self.TIER_G:
            return [self.TIER_H, self.TIER_H_NAME]
        
        if reward_tier == self.TIER_H:
            return [self.TIER_I, self.TIER_I_NAME]

        if reward_tier == self.TIER_I:
            return [self.TIER_J, self.TIER_J_NAME]
        
        if reward_tier == self.TIER_J:
            return "Highest Possible Tier is Tier J"
    
    def roundup(self, x):
        return x if x % 100 == 0 else x + 100 - x % 100
    
    def calculateNextTierProgress(self, reward_points):
        next_tier_number = self.roundup(reward_points)
        return (reward_points / next_tier_number) 

    def parse_json(self, data):
        return json.loads(json.dumps(data))