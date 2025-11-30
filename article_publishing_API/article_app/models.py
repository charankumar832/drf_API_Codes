from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    rolename=models.CharField(max_length=200)

    def __str__(self):
        return self.rolename

class User(AbstractUser):
    role=models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_role', null=True, blank=True)

    def __str__(self):
        return str(self.username)

class Article(models.Model):
    title=models.CharField(max_length=200)
    content=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    wordCount=models.IntegerField()
    createdDate=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=200,default="draft")
    authorID=models.ForeignKey(User, on_delete=models.CASCADE, related_name='aticle_author')

    def __str__(self):
        return self.title



