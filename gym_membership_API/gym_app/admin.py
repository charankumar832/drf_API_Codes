from django.contrib import admin
from .models import Role, User, Membership

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Membership)