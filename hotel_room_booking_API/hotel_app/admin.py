from django.contrib import admin
from .models import Role, User, Room, Booking


admin.site.register(User)
admin.site.register(Role)
admin.site.register(Room)
admin.site.register(Booking)