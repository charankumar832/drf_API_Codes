from django.contrib import admin
from .models import User, Product, Order

admin.site.register(Order)
admin.site.register(Product)
admin.site.register(User)