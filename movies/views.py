from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Rating


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {
        'movies': movies
    })


@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        score = request.POST.get("score")
        if score:
            Rating.objects.update_or_create(
                user=request.user,
                movie=movie,
                defaults={'score': score}
            )
            return redirect('movie_detail', movie_id=movie.id)

    ratings = Rating.objects.filter(movie=movie)

    if ratings.exists():
        average = sum([r.score for r in ratings]) / ratings.count()
    else:
        average = 0

    user_rating = Rating.objects.filter(user=request.user, movie=movie).last()

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'average': average,
        'user_rating': user_rating
    })
