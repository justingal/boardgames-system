from django.db import models
from django.contrib.auth.models import User
from core.models import Organization, Game

class Event(models.Model):
    TABLE_SIZES = [
        ('S', 'Mažas'),
        ('M', 'Vidutinis'),
        ('L', 'Didelis'),
    ]

    VISIBILITY_CHOICES = [
        ('public', 'Viešas – visi gali prisijungti'),
        ('private', 'Privatus – tik pakviestieji'),
    ]

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='events')

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)  # Vieta (vietoj miesto)

    table_size = models.CharField(max_length=1, choices=TABLE_SIZES, default='M')
    perks = models.TextField(blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')

    is_repeating = models.BooleanField(default=False)
    repeat_days = models.CharField(max_length=100, blank=True)  # Pvz: "Mon,Wed,Fri"
    first_player_is_organizer = models.BooleanField(default=False)
    organizers = models.ManyToManyField(User, related_name='organized_events', blank=True)
    games = models.ManyToManyField(Game, blank=True, related_name='events')
    players = models.ManyToManyField(User, blank=True, related_name='events_joined')

    created_at = models.DateTimeField(auto_now_add=True)

    def join_player(self, user):
        """Add player to event and handle first_player_is_organizer logic"""
        if not self.players.filter(id=user.id).exists():
            self.players.add(user)
            # If this is the first player and first_player_is_organizer is True
            if self.first_player_is_organizer and self.players.count() == 1:
                self.organizers.add(user)
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.title} ({self.organization.name})"
