from rest_framework import serializers
from .models import User, Role, Book, Borrow

# class BorrowSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Borrow
#         fields="__all__"

# class BookSerializer(serializers.ModelSerializer):
#     borrow_book=BorrowSerializer(many=True, read_only=True)
#     class Meta:
#         model=Book
#         fields="__all__"

# class UserSerializer(serializers.ModelSerializer):
#     borrow_user=BorrowSerializer(many=True, read_only=True)
#     class Meta:
#         model=User
#         fields="__all__"

# class RoleSerializer(serializers.ModelSerializer):
#     user_role=UserSerializer(many=True, read_only=True)
#     class Meta:
#         model=Role
#         fields="__all__"

class RoleSerializer(serializers.ModelSerializer):    
    class Meta:
        model=Role
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model=User
        fields="__all__"

class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model=Borrow
        fields="__all__"

class BookSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Book
        fields="__all__"




