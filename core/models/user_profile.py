from django.db import models
from django.contrib.auth.models import User
from core.models import Organization

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('organizer', 'Organizer'),
        ('player', 'Player'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='player')

    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"