from rest_framework import serializers
from core.models import Organization, GameCategory, Game
from django.contrib.auth.models import User
from core.models.organization import Membership
from core.serializers.event_serializer import EventSerializer


class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameCategory
        fields = ['id', 'name']


class OrganizationSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # Make categories read-only since we're not using the M2M relationship anymore
    categories = GameCategorySerializer(many=True, read_only=True)
    # Add the new single category field
    category = serializers.CharField()
    is_member = serializers.SerializerMethodField()
    city = serializers.CharField()
    events = EventSerializer(many=True, read_only=True)

    # Add category display name
    category_display = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'description', 'created_by',
            'members', 'categories', 'category', 'category_display',
            'privacy', 'created_at', 'is_member', 'city', 'events'
        ]

    def get_category_display(self, obj):
        """Get the display name for the category"""
        return dict(Organization.CATEGORY_CHOICES).get(obj.category, '')

    def get_is_member(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.members.filter(id=request.user.id).exists()


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'user', 'organization', 'joined_at']
        read_only_fields = ['id', 'user', 'joined_at']