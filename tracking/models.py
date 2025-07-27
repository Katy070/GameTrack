from django.db import models
from django.conf import settings
from games.models import Game
from django.contrib.auth.models import User

class TimePlayed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    total_minutes = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'game')
        verbose_name = 'Time Played'
        verbose_name_plural = 'Time Played Records'

    def __str__(self):
        return f"{self.user.username} - {self.game.title} - {self.total_hours()} hrs"

    def total_hours(self):
        return round(self.total_minutes / 60, 2)

class TimeSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    seconds_played = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def hours_played(self):
        return round(self.seconds_played / 3600, 2)

    def __str__(self):
        return f"{self.user.username} - {self.game.title} - {self.hours_played()} hrs"
