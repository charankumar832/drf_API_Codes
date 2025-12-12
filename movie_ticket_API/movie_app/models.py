from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    rolename=models.CharField(max_length=200)

    def __str__(self):
        return self.rolename
    
class User(AbstractUser):
    role=models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_role', blank=True, null=True)

    def __str__(self):
        return str(self.username)
class Movie(models.Model):
    title=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    basePrice=models.FloatField()
    available=models.BooleanField(default=True)

    def __str__(self):
        return self.title+str(self.basePrice)
    
class Reservation(models.Model):
    customerId=models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservation_user')
    movieId=models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reservation_movie')
    quantity=models.IntegerField()
    discountPct=models.FloatField(default=0)
    gstPct=models.FloatField(default=18)
    serviceFee=models.FloatField(default=50)
    totalAmount=models.FloatField()
    reservationDate=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=200, default='reserved')

    def __str__(self):
        return str(self.customerId.username)+self.totalAmount
    


