from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models import JoinRequest, Invite

User = get_user_model()


class JoinRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = JoinRequest
        fields = ['id', 'user', 'user_email', 'organization', 'event', 'created_at']


class InviteSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = Invite
        fields = ['id', 'invited_user', 'organization', 'event', 'is_accepted', 'created_at', 'organization_name']
