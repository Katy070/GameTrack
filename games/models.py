from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.ManyToManyField(Genre)
    platform = models.ManyToManyField(Platform)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    developer = models.ForeignKey('Developer', on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='game_covers/', blank=True, null=True)

    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

class Developer(models.Model):
    name = models.CharField(max_length=100)
    founded_year = models.IntegerField(blank=True, null=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        return self.reviews.aggregate(avg=Avg('rating'))['avg'] or 0

class Review(models.Model):
    developer = models.ForeignKey(Developer, related_name="reviews", on_delete=models.CASCADE)


class GameStatus(models.Model):
    STATUS_CHOICES = [
        ('backlog', 'Backlog'),
        ('playing', 'Playing'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} - {self.game.title} - {self.status}"