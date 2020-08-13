from django.db import models

# Create your models here.

class CustomerData(models.Model):
      Email_Address = models.CharField(max_length=30)
      Reward_Points = models.CharField(max_length=30)
      Reward_Tier = models.CharField(max_length=30)
      Reward_Tier_Name =  models.CharField(max_length=30)
      Next_Reward_Tier = models.CharField(max_length=30)
      Next_Reward_Tier Name = models.CharField(max_length=30)
      Next_Reward_Tier Progress = models.CharField(max_length=30)