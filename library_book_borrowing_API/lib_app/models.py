from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    rolename=models.CharField(max_length=200)

    def __str__(self):
        return self.rolename
    
class User(AbstractUser):
    role=models.ForeignKey(Role,on_delete=models.CASCADE, related_name='user_role',null=True, blank=True)

    def __str__(self):
        return str(self.username)

class Book(models.Model):
    title=models.CharField(max_length=200)
    author=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    price=models.FloatField()
    available=models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Borrow(models.Model):

    bookId=models.ForeignKey(Book,on_delete=models.CASCADE, related_name='borrow_book')
    memberId=models.ForeignKey(User,on_delete=models.CASCADE, related_name='borrow_user')
    borrowDate=models.DateField(auto_now_add=True)
    returnDate=models.DateField()
    fine=models.FloatField()
    status=models.CharField(max_length=200,default="Borrowed")

    def __str__(self):
        return str(self.bookId.title)+str(self.memberId.username)



