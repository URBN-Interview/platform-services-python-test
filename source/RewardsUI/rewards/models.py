from django.db import models


# Create your models here.

class OrderData(models.Model):
      Email_Address = models.CharField(max_length=30)
      Order_Total = models.IntegerField()
      Reward_Points = models.CharField(max_length=30)
      Reward_Tier = models.CharField(max_length=30)
      Reward_Tier_Name =  models.CharField(max_length=30)
      Next_Reward_Tier = models.CharField(max_length=30)
      Next_Reward_Tier_Name = models.CharField(max_length=30)
      Next_Reward_Tier_Progress = models.CharField(max_length=30)


      @property
      def get_points(self, total):
          return int(float(total))

      @property
      def get_tier(self, total):
          if total < 100:
              return "not yet"
          elif total < 200:
              return "A"
          elif total < 300:
              return "B"
          elif total < 400:
              return "C"
          elif total < 500:
              return "D"
          elif total < 600:
              return "E"
          elif total < 700:
              return "F"
          elif total < 800:
              return "G"
          elif total < 900:
              return "H"
          elif total < 1000:
              return "I"
          else:
              return "J"

      @property
      def get_tier_name(self, tiername):
        #hard-code for brute force solution (ideal : pull from get req or other file)
        if tiername == "J":
          return "No more upgrades!"
        elif tiername == "A":
          return "5% off purchase"
        elif tiername == "B":
          return "10% off purchase"
        elif tiername == "C":
          return "15% off purchase"
        elif tiername == "D":
          return "20% off purchase"
        elif tiername == "E":
          return "25% off purchase"
        elif tiername == "F":
          return "30% off purchase"
        elif tiername == "G":
          return "35% off purchase"
        elif tiername == "H":
          return "40% off purchase"
        elif tiername == "I":
          return "45% off purchase"
        elif tiername == "J":
          return "50% off purchase"


      @property
      def get_next_tier(self, currentTier):
        if currentTier == "not yet":
          return "A"
        elif currentTier == "A":
          return "B"
        elif currentTier == "B":
          return "C"
        elif currentTier == "C":
          return "D"
        elif currentTier == "D":
          return "E"
        elif currentTier == "E":
          return "F"
        elif currentTier == "F":
          return "G"
        elif currentTier == "G":
          return "H"
        elif currentTier == "H":
          return "I"
        elif currentTier == "I":
          return "J"
        elif currentTier == "J":
          return "No more"

      @property
      def get_progress(self, total):
        # return round(float(total) / )

        #place holder
        return "0.5"

      def save(self, *args, **kwargs):
        # 'not callable' py-lint error - vs code problem?
        self.Reward_Points = self.get_points(self, self.Order_Total)
        self.Reward_Tier = self.get_tier(self, self.Order_Total)
        self.Reward_Tier_Name = self.get_tier_name(self, self.Reward_Tier)
        self.Next_Reward_Tier = self.get_next_tier(self, self.Reward_Tier_Name)
        self.Next_Reward_Tier_Name = self.get_tier_name(self, self.Next_Reward_Tier)
        self.Next_Reward_Tier_Progress = self.get_progress()

        super(OrderData, self).save(*args, **kwargs)