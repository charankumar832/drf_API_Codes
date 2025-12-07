from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    role=models.CharField(max_length=200)

    def __str__(self):
        return self.role
class User(AbstractUser):
    roleobj=models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_role', null=True, blank=True)

    def __str__(self):
        return str(self.username)
    
class Shipment(models.Model):
    tracking_number=models.CharField(max_length=200)
    Shipment_status=models.CharField(max_length=200)
    receiver_name=models.CharField(max_length=200)
    senderobj=models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipment_user',null=True, blank=True)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tracking_number+self.Shipment_status+self.receiver_name
    
