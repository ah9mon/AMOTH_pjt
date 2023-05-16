from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404

# rest_framework
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Models
from .models import Movie

# Serializers
from .serializers import MovieSerializer

# requests
import requests

# ast
import ast

# TMDB API
TMDB_api_key = settings.API_KEY
BASE_url = "https://api.themoviedb.org/3/movie/"

# Create your views here.

# tmdb에서 영화리스트 데이터 가져오기 
@api_view(['GET', 'POST']) # gpt, 내가 본 영화등록 : POST / CRUD의 사운드 트랙 게시글은 GET
def get_or_post_movies_data(request):
    movies_in_DB = Movie.objects.all()
    # params 로 {movies_id:[1,2,3,4]} 형태로 movies_id 보낸거 받기
    # response에서 TMDB API나 DB에서 검색할 때 쓸 movie_id 추출
    movies_id_str = request.GET.get("movies_id", "")
    try :
        movies_id_list = ast.literal_eval(movies_id_str)
    except (ValueError, SyntaxError):
        movies_id_list = []
        # return HttpResponseNotFound("Invalid movies_id data")

    existing_movies = [] 
    new_movies_id = [] 
    new_movies = [] # DB에 없는 영화 객체들을 담을 리스트

    # DB에 존재하는 영화인지 아닌지 찾기
    for movie_id in movies_id_list:
        
        # 같은 movie_id를 가진 영화가 있는지 찾기 (DB에 존재하는 영화인지)
        existing_movie = movies_in_DB.filter(movie_id=movie_id).first()
        
        if existing_movie: 
            existing_movies.append(existing_movie)
        else:
            new_movies_id.append(movie_id)
            
    if request.method == "POST":
        
        # 반복문으로 영화 데이터 API로 가져오기 
        for new_movie_id in new_movies_id:
            # TMDB API로 GET 요청을 보내 영화 데이터 가져오기
            url = f'{BASE_url}/{new_movie_id}?api_key={TMDB_api_key}'
            res = requests.get(url)
            if res.ok:
                movie_data = res.json() # api로 요청한 영화 데이터 
                
                # 객체 형태로 데이터 저장 
                movie = Movie()
                movie.movie_id = movie_data.get("id")
                movie.title = movie_data.get("title")
                movie.overview = movie_data.get("poster_path")
                movie.release_date = movie_data.get("overview")
                movie.poster_path = movie_data.get("release_date")
                movie.save() 
                
                # 이번 요청에서 저장한 movie 객체 담기
                new_movies.append(movie)

        movies = new_movies + existing_movies # 요청받은 영화들을 합쳐서 보내기

    elif request.method == "GET":

        # create form으로 이동할 때 영화 선택에 필요한 모든 영화 데이터 가져오기
        if not existing_movies and not new_movies: # 둘다 비었으면 모든 영화데이터를 요청
            movies = movies_in_DB
        
        # create시 영화 한개만 요청할때 처리 
        else: 
            movies = existing_movies

    serializer = MovieSerializer(movies, many=True)
    serialized_movies = serializer.data
    return Response(serialized_movies)