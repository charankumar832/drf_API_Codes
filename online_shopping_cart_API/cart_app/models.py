from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    rolename=models.CharField(max_length=200)

    def __str__(self):
        return self.rolename


class User(AbstractUser):
    role=models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_role', null=True, blank=True)

    def __str__(self):
        return str(self.username)
    
class Product(models.Model):
    name=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    price=models.FloatField()
    stock=models.IntegerField()

    def __str__(self):
        return self.name
class Cart(models.Model):
    customerId=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_user')
    productId=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_cart')
    quantity=models.IntegerField()
    discountPct=models.FloatField(default=0)
    taxPct=models.FloatField(default=12)
    totalPrice=models.FloatField()
    addedDate=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=200, default='in_cart')

    def __str__(self):
        return str(self.customerId.username)+str(self.productId.name)
    
    
    