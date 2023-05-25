
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404

# rest_framework
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# Models
from .models import Movie

# Serializers
from .serializers import MovieSerializer

# requests
import requests

# TMDB API
TMDB_api_key = settings.API_KEY
TMDB_auth = settings.TMDB_AUTH
BASE_url = "https://api.themoviedb.org/3/search/movie"

# Create your views here.


################################
############ API ###############
################################

def get_movie_in_tmdbapi(movie_title, release_data):
    '''
    TMDB API를 이용해서 영화 데이터 가져오는 함수  
    '''
    query = movie_title
    language = "en-US"
    primary_release_year = release_data[:4]
    url = f'{BASE_url}?query={query}&language={language}&primary_release_year={primary_release_year}&api_key={TMDB_api_key}&page=1'
    headers = {
        "accept": "application/json",
        "Authorization": f'Bearer {TMDB_api_key}'
    }
    res = requests.get(url, headers=headers)
    movie_data = res.json().get('results') # api로 요청한 영화 데이터

    if movie_data:
        data = {
            "movie_id" : movie_data[0].get('id'),
            "title" : movie_data[0].get('title'),
            "overview" : movie_data[0].get('overview'),
            "release_date" : movie_data[0].get('release_date'),
            "poster_path" : movie_data[0].get('poster_path'),
            "backdrop_path" : movie_data[0].get('backdrop_path')
        }

        return data
    else:
        return None

def detect_lang(q):
    papago_detect_url = f"http://127.0.0.1:8004/api/papago/detect?q={q}" # 검색어만 prams넣고 보내기
    detected = requests.get(papago_detect_url)
    return detected.json().get('langCode')

def translate_q(q,lang):
    papago_translate_url = f"http://127.0.0.1:8004/api/papago/translate?q={q}&lang={lang}"  # 검색어와 언어감지 결과 같이 보내기 
    translated = requests.get(papago_translate_url)
    return translated.json().get('message').get('result').get('translatedText')

###################################
###################################
###################################

# tmdb에서 영화리스트 데이터 가져오기 
@api_view(['POST']) # gpt, 내가 본 영화등록 : POST / CRUD의 사운드 트랙 게시글은 GET
def movies_data(request):
    '''
    front에서 줘야할 데이터 
    { 
    	movies :  {
    		movie1 : {
    			Title : 'title', 
    			Reason for Recommendation: 'reason'
    		}, 
    		movie2 : {
    			Title2:'title', 
    			Reason:'reason'
    		},
    	    ...
        }
    }
    '''

    if request.method == "POST":
        existing_movies = [] 
        new_movies = [] # DB에 없는 영화 객체들을 담을 리스트

        movies = request.data.get("movies")

        if movies:
            for key, value in movies.items():
                title = value.get('title')
                
                release_date = value.get('release_date')
                if not release_date:
                    release_date = value.get('release_data')
                
                movie = get_movie_in_tmdbapi(title,release_date) # TMDB에서 영화 데이터 가져오기 

                # gpt가 잘못된 데이터 줬으면 아래 코드 생략
                if not movie:
                    continue
                
                movie_id = movie.get('movie_id')

                try:
                    existing_movie = Movie.objects.get(movie_id = movie_id)
                except:
                    existing_movie = None

                if existing_movie:
                    existing_movies.append(existing_movie)
                else:
                    # 객체 형태로 데이터 저장 
                    new_movie = Movie()
                    new_movie.movie_id = movie_id
                    new_movie.title = movie.get("title")
                    new_movie.overview = movie.get("overview")
                    new_movie.release_date = movie.get("release_date")
                    new_movie.poster_path = movie.get("poster_path")
                    new_movie.backdrop_path = movie.get("backdrop_path")
                    new_movie.save() 

                    # 이번 요청에서 저장한 movie 객체 담기
                    new_movies.append(new_movie)

            movies_data = existing_movies + new_movies 

        else: # create form으로 이동할 때 영화 선택에 필요한 모든 영화 데이터 가져오기
            movies_data = Movie.objects.all()
 
        serializer = MovieSerializer(movies_data, many =True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    




# 영화 검색 1개 기능 (DB에 있는 거로 없으면)
@api_view(['GET'])
def get_movie_in_db(request):
    q = request.GET.get('q') # 검색어가 params로 넘어옴
    lang = detect_lang(q) # 검색어 언어감지
    print(lang)
    if lang != "en":  
        translated_text = translate_q(q,lang) # 검색어 영어로 번역
    else:
        translated_text = q
    print(translated_text)
    translated_text_list = translated_text.split() # 검색
    print(translated_text_list)

    find_movies = []
    movies = Movie.objects.all()
    for movie in movies:
        for text in translated_text_list :
            if text in movie.title and text != 'The':
                find_movies.append(movie)
                continue
    find_movies = sorted(find_movies, key=lambda x: -1 * find_movies.count(x))
    temp = []
    for movie in find_movies:
        if movie not in temp:
            temp.append(movie)
    find_movies = temp
    serializer = MovieSerializer(find_movies, many=True)
    return Response(serializer.data)