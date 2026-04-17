from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    image = models.URLField(blank=True, null=True)
    release_year = models.IntegerField()

    def _str_(self):
        return self.title


class Rating(models.Model):
    RATING_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    score = models.IntegerField(choices=RATING_CHOICES)

    def _str_(self):
        return f"{self.user.username} rated {self.movie.title} - {self.score}"
