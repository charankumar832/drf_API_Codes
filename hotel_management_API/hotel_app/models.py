from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    rolename=models.CharField(max_length=200)

    def __str__(self):
        return self.rolename

class User(AbstractUser):
    role=models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_rolename',null=True, blank=True)

    def __str__(self):
        return str(self.username)
    
class Booking(models.Model):
    customerID=models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_customer')
    roomType=models.CharField(max_length=200)
    nights=models.IntegerField()
    basePrice=models.FloatField()
    discount=models.FloatField(default=0.0)
    totalPrice=models.FloatField()
    bookingDate=models.DateTimeField(auto_now_add=True)
    status=models.CharField(default="pending")

    def __str__(self):
        return self.customerID.username+" is in "+self.roomType
    
