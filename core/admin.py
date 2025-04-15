from django.contrib import admin
from .models import Game, UserGame
from .models import Event

admin.site.register(Game)
admin.site.register(UserGame)
admin.site.register(Event)