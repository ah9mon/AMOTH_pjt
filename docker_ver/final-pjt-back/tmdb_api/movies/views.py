from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests

from .models import Movie
from .serializers import MovieSerializer

TMDB_api_key = settings.API_KEY
BASE_url = "https://api.themoviedb.org/3/search/movie"

def get_movie_in_tmdbapi(movie_title, release_date):
    query = movie_title
    language = "en-US"
    primary_release_year = release_date[:4]
    url = f"{BASE_url}?query={query}&language={language}&primary_release_year={primary_release_year}&api_key={TMDB_api_key}&page=1"
    headers = {
        "accept": "application/json"
    }
    res = requests.get(url, headers=headers)
    movie_data = res.json().get("results")

    if movie_data:
        data = {
            "movie_id": movie_data[0].get("id"),
            "title": movie_data[0].get("title"),
            "overview": movie_data[0].get("overview"),
            "release_date": movie_data[0].get("release_date"),
            "poster_path": movie_data[0].get("poster_path"),
            "backdrop_path": movie_data[0].get("backdrop_path")
        }
        return data
    else:
        return None

def detect_lang(q):
    papago_detect_url = f"http://localhost:8004/api/papago/detect?q={q}"
    detected = requests.get(papago_detect_url)
    return detected.json().get("langCode")

def translate_q(q, lang):
    papago_translate_url = f"http://localhost:8004/api/papago/translate?q={q}&lang={lang}"
    translated = requests.get(papago_translate_url)
    return translated.json().get("message").get("result").get("translatedText")

@api_view(["POST"])
def movies_data(request):
    movies = request.data.get("movies")
    existing_movies = []
    new_movies = []

    if movies:
        for key, value in movies.items():
            title = value.get("title")
            release_date = value.get("release_date") or value.get("release_data")

            movie = get_movie_in_tmdbapi(title, release_date)
            if not movie:
                continue

            movie_id = movie.get("movie_id")
            existing_movie = Movie.objects.filter(movie_id=movie_id).first()

            if existing_movie:
                existing_movies.append(existing_movie)
            else:
                new_movie = Movie(
                    movie_id=movie_id,
                    title=movie.get("title"),
                    overview=movie.get("overview"),
                    release_date=movie.get("release_date"),
                    poster_path=movie.get("poster_path"),
                    backdrop_path=movie.get("backdrop_path")
                )
                new_movie.save()
                new_movies.append(new_movie)

    movies_data = existing_movies + new_movies if movies else Movie.objects.all()
    serializer = MovieSerializer(movies_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_movie_in_db(request):
    q = request.GET.get("q")
    lang = detect_lang(q)
    if lang != "en":
        translated_text = translate_q(q, lang)
    else:
        translated_text = q

    translated_text_list = translated_text.split()

    find_movies = Movie.objects.filter(
        title__icontains=translated_text_list[0],
        title__iregex=r"\y(?!The)\w+\y"
    ).distinct().order_by("-pk")

    serializer = MovieSerializer(find_movies, many=True)
    return Response(serializer.data)
