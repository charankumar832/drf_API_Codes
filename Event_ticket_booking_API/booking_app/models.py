from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    rolename=models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.rolename
    
class User(AbstractUser):
    role=models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_role',null=True, blank=True)

    def __str__(self):
        return str(self.username)

class Ticket(models.Model):
    customerId=models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_user')
    eventName=models.CharField(max_length=200,default='Rock Concert')
    category=models.CharField(max_length=200)
    quantity=models.IntegerField()
    basePrice=models.FloatField()
    discountPct=models.FloatField(default=0)
    serviceFee=models.FloatField(default=100)
    gstPct=models.FloatField(default=12)
    totalAmount=models.FloatField()
    bookingDate=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=200,default='booked')

    def __str__(self):
        return self.eventName
    
