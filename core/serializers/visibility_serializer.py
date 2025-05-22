from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models import JoinRequest, Invite

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Simple user serializer for nested user data"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class JoinRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Pilnas user objektas su visais duomenimis
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = JoinRequest
        fields = ['id', 'user', 'user_email', 'user_username', 'organization', 'event', 'created_at']
        read_only_fields = ['created_at']


class InviteSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Invite
        fields = ['id', 'invited_user', 'organization', 'organization_name', 'event', 'event_title', 'is_accepted', 'created_at']
        read_only_fields = ['is_accepted', 'created_at']