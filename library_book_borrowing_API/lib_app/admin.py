from django.contrib import admin
from .models import Role, User, Book, Borrow

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Borrow)