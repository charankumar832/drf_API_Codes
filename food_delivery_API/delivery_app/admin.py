from django.contrib import admin
from .models import Order, User, Role

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Order)

