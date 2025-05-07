from rest_framework import serializers
from core.models import UserProfile, Organization
from django.contrib.auth.models import User


class OrganizationSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']


class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfileFullSerializer(serializers.ModelSerializer):
    user = UserFullSerializer()
    organization = OrganizationSimpleSerializer(read_only=True, required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ['role', 'organization', 'user']

    def to_representation(self, instance):
        # Standartinė reprezentacija
        representation = super().to_representation(instance)

        # Patikrinkime ar organization yra None ir pateikime saugų objektą
        if representation['organization'] is None:
            representation['organization'] = {
                'id': None,
                'name': None
            }

        return representation