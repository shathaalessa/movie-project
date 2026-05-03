from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Movie, Rating

@login_required
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
            score = int(score)
            Rating.objects.update_or_create(
                user=request.user,
                movie=movie,
                defaults={'score': score}
            )
            return redirect('movies:movie_detail', movie_id=movie.id)

    ratings = Rating.objects.filter(movie=movie)

    if ratings.exists():
        average = sum(r.score for r in ratings) / ratings.count()
    else:
        average = 0

    user_rating = Rating.objects.filter(user=request.user, movie=movie).last()

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'average': average,
        'user_rating': user_rating
    })


@login_required
def add_movie(request):
    if request.method == "POST":
        Movie.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            genre=request.POST["genre"],
            image=request.POST["image"],
            release_year=int(request.POST["release_year"])
        )
        return redirect("movies:movie_list")

    return render(request, "movies/add_movie.html")


@login_required
def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        movie.title = request.POST["title"]
        movie.description = request.POST["description"]
        movie.genre = request.POST["genre"]
        movie.image = request.POST["image"]
        movie.release_year = int(request.POST["release_year"])
        movie.save()

        return redirect("movies:movie_detail", movie_id=movie.id)

    return render(request, "movies/update_movie.html", {"movie": movie})


@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect("movies:movie_list")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("movies:movie_list")
        else:
            return render(request, "movies/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "movies/login.html")


def user_logout(request):
    logout(request)
    return redirect("movies:login")


def user_register(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        e = request.POST.get("email")

        user = User.objects.create_user(username=u, password=p, email=e)
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect("movies:login")

    return render(request, "movies/register.html")
