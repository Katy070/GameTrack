from django.db import models
from django.contrib.auth.models import User
from games.models import Game

class Review(models.Model):
    game = models.ForeignKey(Game, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['game', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.game.title} ({self.rating}★)"
