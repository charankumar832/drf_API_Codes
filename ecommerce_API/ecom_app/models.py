from django.db import models
from django.contrib.auth.models import AbstractUser

class Product(models.Model):
    name=models.CharField(max_length=200, unique=True)
    category=models.CharField(max_length=200)
    price=models.FloatField()
    stock=models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    role=models.CharField(choices=[('ADMIN','ADMIN'),('CUSTOMER','CUSTOMER')])

    def __str__(self):
        return str(self.username)
    
class Order(models.Model):
    productID=models.ForeignKey(Product,on_delete=models.CASCADE, related_name='order_product')
    quantity=models.IntegerField()
    totalPrice=models.FloatField() #to be calculated using quantity and price of product
    orderDate=models.DateTimeField(auto_now_add=True)
    status=models.CharField(default="pending")
    customerID=models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')

    def __str__(self):
        return self.productID.name+self.quantity