from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class RewardTier(models.Model):
    reward_tier_name = models.CharField(blank=True, max_length=400)

class User(AbstractUser):
    reward_points = models.IntegerField(default=0)
    reward_tier = models.ForeignKey(RewardTier, on_delete=models.CASCADE, default=1)
    # pass

# class ExtendedUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
#     reward_points = models.IntegerField(default=0)
#     reward_tier = models.CharField(blank=True, max_length=1)