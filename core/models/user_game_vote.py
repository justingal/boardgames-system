# core/models/user_game_vote.py

from django.db import models
from django.conf import settings
from core.models import Event, Game

class UserGameVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()  # Pvz.: 1, 2, 3... mažesnis = svarbiau

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event', 'game')  # Kad tas pats žmogus negalėtų prabalsuoti už tą patį žaidimą daugiau nei vieną kartą

    def __str__(self):
        return f"{self.user.email} voted {self.rank} for {self.game.title} in {self.event.title}"
