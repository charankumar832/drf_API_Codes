from rest_framework import serializers
from .models import User, Role, Membership

class MembershipSerializer(serializers.ModelSerializer):
    # membership_user=serializers.StringRelatedField(read_only=False, queryset=User.objects.all())
    # member=serializers.StringRelatedField(source='membership_user', read_only=True)
    class Meta:
        model=Membership
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    # membership_user=MembershipSerializer(many=True, read_only=True)
    # user_role=serializers.StringRelatedField(read_only=False, queryset=Role.objects.all())
    # role=serializers.StringRelatedField(source='user_role', read_only=True)
    class Meta:
        model=User
        fields="__all__"

class RoleSerializer(serializers.ModelSerializer):
    # user_role=UserSerializer(many=True, read_only=True)
    class Meta:
        model=Role
        fields="__all__"