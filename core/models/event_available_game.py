# core/models/event_available_game.py
from django.db import models
from django.conf import settings
from core.models import Event, Game

class EventAvailableGame(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='available_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'game', 'added_by')

    def __str__(self):
        return f"{self.game.title} į {self.event.title} ({self.added_by.email})"
