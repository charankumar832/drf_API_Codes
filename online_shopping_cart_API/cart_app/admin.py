from django.contrib import admin
from .models import User, Role, Cart, Product

admin.site.register(User)
admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(Role)
