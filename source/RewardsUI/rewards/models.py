from django.db import models


# Create your models here.

class OrderData(models.Model):
      Email_Address = models.CharField(max_length=30)
      Order_Total = models.FloatField()
      Reward_Points = models.CharField(max_length=30)
      Reward_Tier = models.CharField(max_length=30)
      Reward_Tier_Name =  models.CharField(max_length=30)
      Next_Reward_Tier = models.CharField(max_length=30)
      Next_Reward_Tier_Name = models.CharField(max_length=30)
      Next_Reward_Tier_Progress = models.CharField(max_length=30)


      # @property
      # def get_points(self):
      #     points = (float(self.Order_Total))
      #     return points

      @property
      def get_tier(self):
          if int(float(self.Order_Total)) < 100:
              return "not yet"
          elif int(float(self.Order_Total)) < 200:
              return "A"
          elif int(float(self.Order_Total)) < 300:
              return "B"
          elif int(float(self.Order_Total)) < 400:
              return "C"
          elif int(float(self.Order_Total)) < 500:
              return "D"
          elif int(float(self.Order_Total)) < 600:
              return "E"
          elif int(float(self.Order_Total)) < 700:
              return "F"
          elif int(float(self.Order_Total)) < 800:
              return "G"
          elif int(float(self.Order_Total)) < 900:
              return "H"
          elif int(float(self.Order_Total))< 1000:
              return "I"
          else:
              return "J"

      @property
      def get_tier_name(self):
        #hard-code for brute force solution (ideal : pull from get req or other file)
        if self.Reward_Tier == "J":
          return "No more upgrades!"
        elif self.Reward_Tier == "A":
          return "5% off purchase"
        elif self.Reward_Tier == "B":
          return "10% off purchase"
        elif self.Reward_Tier == "C":
          return "15% off purchase"
        elif self.Reward_Tier == "D":
          return "20% off purchase"
        elif self.Reward_Tier == "E":
          return "25% off purchase"
        elif self.Reward_Tier == "F":
          return "30% off purchase"
        elif self.Reward_Tier == "G":
          return "35% off purchase"
        elif self.Reward_Tier == "H":
          return "40% off purchase"
        elif self.Reward_Tier == "I":
          return "45% off purchase"
        elif self.Reward_Tier == "J":
          return "50% off purchase"


      @property
      def get_next_tier(self):
        if self.Reward_Tier_Name == "not yet":
          return "A"
        elif self.Reward_Tier_Name == "A":
          return "B"
        elif self.Reward_Tier_Name == "B":
          return "C"
        elif self.Reward_Tier_Name == "C":
          return "D"
        elif self.Reward_Tier_Name == "D":
          return "E"
        elif self.Reward_Tier_Name == "E":
          return "F"
        elif self.Reward_Tier_Name == "F":
          return "G"
        elif self.Reward_Tier_Name == "G":
          return "H"
        elif self.Reward_Tier_Name == "H":
          return "I"
        elif self.Reward_Tier_Name == "I":
          return "J"
        elif self.Reward_Tier_Name == "J":
          return "No more"

      @property
      def get_next_tier_name(self):
        #hard-code for brute force solution (ideal : pull from get req or other file)
        if self.Next_Reward_Tier == "J":
          return "No more upgrades!"
        elif self.Next_Reward_Tier == "A":
          return "5% off purchase"
        elif self.Next_Reward_Tier == "B":
          return "10% off purchase"
        elif self.Next_Reward_Tier == "C":
          return "15% off purchase"
        elif self.Next_Reward_Tier == "D":
          return "20% off purchase"
        elif self.Next_Reward_Tier == "E":
          return "25% off purchase"
        elif self.Next_Reward_Tier == "F":
          return "30% off purchase"
        elif self.Next_Reward_Tier == "G":
          return "35% off purchase"
        elif self.Next_Reward_Tier == "H":
          return "40% off purchase"
        elif self.Next_Reward_Tier == "I":
          return "45% off purchase"
        elif self.Next_Reward_Tier == "J":
          return "50% off purchase"

      @property
      def get_progress(self):
        # return round(float(total) / )

        #place holder
        return "0.5"

      def save(self, *args, **kwargs):
        # 'not callable' py-lint error - vs code problem?
        # or perhaps I need separate classes for every field I am calculating the values for, and import them here?
        self.Reward_Points = self.Order_Total
        self.Reward_Tier = self.get_tier
        self.Reward_Tier_Name = self.get_tier_name
        self.Next_Reward_Tier = self.get_next_tier
        self.Next_Reward_Tier_Name = self.get_next_tier_name
        self.Next_Reward_Tier_Progress = self.get_progress

        super(OrderData, self).save(*args, **kwargs)