from rest_framework import serializers
from .models import Role, User, Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Article
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    aticle_author=ArticleSerializer(many=True, read_only=True)
    class Meta:
        model=User
        fields="__all__"

    
class RoleSerializer(serializers.ModelSerializer):
    user_role=UserSerializer(many=True, read_only=True)
    class Meta:
        model=Role
        fields="__all__"

