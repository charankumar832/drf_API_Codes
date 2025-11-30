from django.contrib import admin
from .models import Role, User, Booking

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Booking)