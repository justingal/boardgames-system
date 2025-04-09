from django.db import models
from django.contrib.auth.models import User
from .game import Game

class UserGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collection')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} – {self.game.title}"
