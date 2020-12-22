from django.db import models

# Create your models here.
class Rewards(models.Model):
    email_address = models.EmailField(max_length=256)
    reward_points = models.CharField(max_length=256)
    reward_tier = models.CharField(max_length=1)
    reward_tier_name = models.CharField(max_length=30)
    next_reward_tier = models.CharField(max_length=1)
    next_reward_tier_name = models.CharField(max_length=30)
    progress = models.DecimalField(decimal_places=1)
