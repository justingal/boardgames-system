from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Organization, UserProfile, Membership

class OrganizerRegisterSerializer(serializers.ModelSerializer):
    organization = serializers.DictField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'organization']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        org_data = validated_data.pop('organization')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        org = Organization.objects.create(
            name=org_data['name'],
            description=org_data.get('description', ''),
            privacy=org_data.get('privacy', 'protected'),
            created_by=user,
            city=org_data.get('city', 'vilnius')
        )

        # add category if string given
        category = org_data.get('category')
        if category:
            from core.models import GameCategory
            cat_obj, _ = GameCategory.objects.get_or_create(name=category)
            org.categories.add(cat_obj)

        # create profile and membership
        UserProfile.objects.create(user=user, role='organizer', organization=org)
        Membership.objects.create(user=user, organization=org)

        return user