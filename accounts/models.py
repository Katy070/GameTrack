from django.db import models
from django.contrib.auth.models import User
from games.models import Game

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='avatars/', default='media/default-avatar.png.jpg', blank=True)
    favorite_games = models.ManyToManyField(Game, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"