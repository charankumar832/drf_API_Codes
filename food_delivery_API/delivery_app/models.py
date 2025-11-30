from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    rolename=models.CharField(max_length=200)
    def __str__(self):
        return self.rolename


class User(AbstractUser):
    role=models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_rolename', null=True, blank=True)

    def __str__(self):
        return str(self.username)
    

class Order(models.Model):
    customerID=models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
    items=models.CharField(max_length=200)
    baseAmount=models.FloatField()
    deliveryFee=models.FloatField(default=50.0)
    discountPct=models.FloatField(default=0.0)
    gstPct=models.FloatField(default=5.0)
    finalAmount=models.FloatField()
    orderDate=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=200)

    def __str__(self):
        return self.items
    
    

