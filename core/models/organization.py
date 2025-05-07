from django.db import models
from django.contrib.auth.models import User
from core.models import Game

class GameCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Vieša'),
        ('protected', 'Pusiau privati'),
        ('private', 'Privati'),
    ]

    CITY_CHOICES = [
        ('vilnius', 'Vilnius'),
        ('kaunas', 'Kaunas'),
        ('klaipeda', 'Klaipėda'),
        ('siauliai', 'Šiauliai'),
        ('panevezys', 'Panevėžys'),
    ]

    # Hardcoded category choices
    CATEGORY_CHOICES = [
        ('classic_strategic', 'Klasikiniai & Strateginiai'),
        ('rpg', 'RPG (Role-playing games)'),
        ('miniature_games', 'Miniatiūrų žaidimai'),
        ('party_social', 'Vakarėlių ir socialiniai žaidimai'),
        ('children_games', 'Vaikų žaidimai'),
        ('educational', 'Edukaciniai žaidimai'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizations_created')
    members = models.ManyToManyField(User, through='Membership', related_name='organizations_joined', blank=True)
    categories = models.ManyToManyField(GameCategory, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='classic_strategic')  # New field for hardcoded category
    games = models.ManyToManyField(Game, blank=True)
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=50, choices=CITY_CHOICES, default='vilnius')

    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='memberships')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'organization')

    def __str__(self):
        return f"{self.user.username} in {self.organization.name}"