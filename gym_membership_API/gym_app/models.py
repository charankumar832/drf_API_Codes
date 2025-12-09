from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    rolename=models.CharField(choices=[('MEMBER','MEMBER'),('ADMIN','ADMIN')])

    def __str__(self):
        return self.rolename
class User(AbstractUser):
    role=models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_role', null=True, blank=True)

    def __str__(self):
        return str(self.username)
    
class Membership(models.Model):

    memberId=models.ForeignKey(User, on_delete=models.CASCADE, related_name='membership_user')
    planType=models.CharField(max_length=200)
    baseFee=models.FloatField()
    discountPct=models.FloatField(default=0)
    taxPct=models.FloatField(default=18)
    totalFee=models.FloatField()
    startDate=models.DateField(auto_now_add=True)
    endDate=models.DateField()
    status=models.CharField(max_length=200, default="active")

    def __str__(self):
        return self.planType+str(self.memberId.username)