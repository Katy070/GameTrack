from django.contrib import admin
from .models import Game, Genre, Platform, Developer

admin.site.register(Game)
admin.site.register(Developer)
admin.site.register(Genre)
admin.site.register(Platform)
