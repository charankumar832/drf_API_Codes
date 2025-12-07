from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    rolename=models.CharField(max_length=200)

    def __str__(self):
        return self.rolename
    
class User(AbstractUser):
    role=models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_role',null=True, blank=True)

    def __str__(self):
        return str(self.username)
    
class Rental(models.Model):
    customerId=models.ForeignKey(User, on_delete=models.CASCADE, related_name='rental_user')
    carType=models.CharField(max_length=200)
    days=models.IntegerField()
    baseRate=models.FloatField()
    insuranceFee=models.FloatField(default=500)
    discountPct=models.FloatField()
    totalCost=models.FloatField()
    rentalDate=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=200, default="booked")

    def __str__(self):
        return self.carType+self.baseRate