from django.db import models

# Create your models here.
class Rewards(models.Model):
    tier = models.CharField(max_length = 1)
    points = models.IntegerField()
    rewardName = models.CharField(max_length = 50)

    def __str__(self):
        return self.tier

class Customers(models.Model):
    email = models.CharField(max_length = 50)
    rewardPoints = models.IntegerField()
    rewardTier = models.CharField(max_length = 1, blank = true)
    rewardTierName = models.CharField(max_length = 50, blank = true)
    nextRewardTier = models.CharField(max_length = 1, blank = true)
    nextRewardtierName = models.CharField(max_length = 50, blank = true)
    nextRewardTierProgress = models.IntegerField(blank = true)

    def __str__(self):
        return self.email
