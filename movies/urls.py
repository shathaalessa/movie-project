from django.urls import path
from . import views

app_name = "movies"
urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('add/', views.add_movie, name='add_movie'),
    path('update/<int:movie_id>/', views.update_movie, name='update_movie'),
    path('delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('my-ratings/', views.my_ratings, name='my_ratings'),

    # Login / Logout
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
]
