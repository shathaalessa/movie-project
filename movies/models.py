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
# ADD MOVIE
from django.contrib.auth.decorators import login_required

@login_required
def add_movie(request):
    if request.method == "POST":
        Movie.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            genre=request.POST["genre"],
            image=request.POST["image"],
            release_year=request.POST["release_year"]
        )
        return redirect("movie_list")

    return render(request, "movies/add_movie.html")


# UPDATE MOVIE
@login_required
def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        movie.title = request.POST["title"]
        movie.description = request.POST["description"]
        movie.genre = request.POST["genre"]
        movie.image = request.POST["image"]
        movie.release_year = request.POST["release_year"]
        movie.save()

        return redirect("movie_detail", movie_id=movie.id)

    return render(request, "movies/update_movie.html", {"movie": movie})


# DELETE MOVIE
@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect("movie_list")
