from django.contrib import admin
from .models import User, Reservation, Role, Movie

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Reservation)
admin.site.register(Movie)