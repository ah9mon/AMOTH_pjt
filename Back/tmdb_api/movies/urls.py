from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('movies', views.get_or_post_movies_data, name="movies"),
]
