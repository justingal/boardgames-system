from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import Organization, UserProfile, Membership, GameCategory


class OrganizerRegisterSerializer(serializers.ModelSerializer):
    organization = serializers.DictField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'organization']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user_data = {k: v for k, v in data.items() if k in ['username', 'email', 'first_name', 'last_name']}
        try:
            validate_password(data['password'], user=User(**user_data))
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        return data

    def create(self, validated_data):
        org_data = validated_data.pop('organization')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )

        org = Organization.objects.create(
            name=org_data['name'],
            description=org_data.get('description', ''),
            privacy=org_data.get('privacy', 'protected'),
            created_by=user,
            city=org_data.get('city', 'vilnius')
        )

        category = org_data.get('category')
        if category:
            cat_obj, _ = GameCategory.objects.get_or_create(name=category)
            org.categories.add(cat_obj)

        UserProfile.objects.create(user=user, role='organizer', organization=org)
        Membership.objects.create(user=user, organization=org)

        return user
