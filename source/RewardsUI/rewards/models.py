from django.db import models

# Create your models here.

class Email(models.Model):
    email = models.CharField(max_length=200)


class Order(models.Model):
    order = models.FloatField(default=0.00)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)

