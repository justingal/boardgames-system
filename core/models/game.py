from django.db import models

class Game(models.Model):
    bgg_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    min_players = models.IntegerField(null=True, blank=True)
    max_players = models.IntegerField(null=True, blank=True)
    playtime_minutes = models.IntegerField(null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
