from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    rolename=models.CharField(choices=[('CUSTOMER','CUSTOMER'),('ADMIN','ADMIN')])

    def __str__(self):
        return self.rolename
    
class User(AbstractUser):
    role=models.ForeignKey(Role,on_delete=models.CASCADE, related_name='user_role',null=True, blank=True)
    
    def __str__(self):
        return str(self.username)

class Room (models.Model):
    roomType=models.CharField(max_length=200)
    baseRate=models.FloatField()
    available=models.BooleanField(default=True)

    def __str__(self):
        return self.roomType+str(self.baseRate)
class Booking(models.Model):
    customerId=models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_user')
    roomId=models.ForeignKey(Room, on_delete=models.CASCADE, related_name='booking_room')
    nights=models.IntegerField()
    discountPct=models.FloatField(default=0)
    taxPct=models.FloatField(default=12)
    serviceFee=models.FloatField(default=200)
    totalCost=models.FloatField()
    bookingDate=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=200, default='booked')

    def __str__(self):
        return self.roomId.roomType+self.customerId.username+str(self.nights)
    
    