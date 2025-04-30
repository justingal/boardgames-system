from django.db import models
from django.contrib.postgres.fields import ArrayField

class Game(models.Model):
    bgg_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    min_players = models.IntegerField(null=True, blank=True)
    max_players = models.IntegerField(null=True, blank=True)
    playtime_minutes = models.IntegerField(null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)
    average_rating = models.FloatField(blank=True, null=True)
    overall_rank = models.IntegerField(blank=True, null=True)
    complexity = models.FloatField(blank=True, null=True)
    recommended_age = models.IntegerField(blank=True, null=True)
    categories = ArrayField(models.CharField(max_length=100), default=list, blank=True)
    mechanics = ArrayField(models.CharField(max_length=100), default=list, blank=True)
    language_dependence = models.CharField(max_length=100, null=True, blank=True)
    best_player_count = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title
