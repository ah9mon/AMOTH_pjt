from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect

# rest_framework
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# models
from .models import User

# serializers
from .serializers import UserSerializer

# requests
import requests

# YOUTUBE API
KAKAO_api_key = settings.API_KEY
USER_url = "https://kapi.kakao.com"
AUTH_url = "https://kauth.kakao.com"

# Create your views here.

def get_userdata(access_token):
    '''
    access_token으로 userdata 가져오는 함수

    param
    access_token : 사용자 정보 요청할 때 사용하는 access_token
    '''

    Authorization = f'Bearer {access_token}'
    header = {
        'Authorization' : Authorization
    }
    user_url = f'{USER_url}/v2/user/me'
    # user 정보 요청 
    user = requests.get(user_url, headers = header)

    return user

def get_access_token(code):
    '''
    인가 code로 access_token 가져오는 함수

    param
    code : access_token 요청할 때 사용하는 인가코드
    '''
    data = {
        'client_id' : KAKAO_api_key,
        'grant_type' : 'authorization_code',
        'redirection_uri' : 'http://127.0.0.1:8000/api/kakao',
        'code' : code
    }
    token_url = f'{AUTH_url}/oauth/token'
    
    # post로 요청 
    token_data = requests.post(token_url, data=data).json()

    access_token = token_data.get('access_token')
    # token_type = token_res.json().get('token_type')
    # refresh_token = token_res.json().get('refresh_token')

    return access_token

###########################
### 카카오 로그인 및 회원가입 ###
###########################

def KakaoLogin(request):
    # 1. 인가 코드 받기 요청 
    redirect_uri = 'http://127.0.0.1:8000/api/kakao/callback'
    url = f'{AUTH_url}/oauth/authorize?client_id={KAKAO_api_key}&redirect_uri={redirect_uri}&response_type=code'
    return redirect(url)

def KakaoCallback(request):
    # 인가 코드 받아서 auth/kakao 에서 auth/kakao/callback으로 리다이렉트돼서 온거임
     
    # 2. 인가 코드로 access token 요청 
    code = request.GET.get('code')
    access_token = get_access_token(code)


    # 3. access_token을 사용해서 사용자 정보 가져오기 
    user = get_userdata(access_token).json()

    # 사용자 정보 Model 형식으로
    nickname = user.get('properties').get('nickname')
    profile_image = user.get('properties').get('profile_image')
    email = user.get('kakao_account').get('email')
    userdata = {
        'nickname' : nickname,
        'profile_image' : profile_image,
        'email' : email
    }

    # 신규 사용자 회원가입 (DB에 저장)
    serializer = UserSerializer(data = userdata) 
    users = User.objects.all()
    if serializer.is_valid(raise_exception=True):
        existing_user = users.filter(email = email)
        if not existing_user: # DB에 없는 사용자면 
            print('회원가입!')
            serializer.save()
    
    context = {
        'access_token' : access_token 
    }
    
    return HttpResponseRedirect(f'http://127.0.0.1:8080/login?access_token={access_token}')

###########################
##### 사용자 로그인 처리 #####
###########################

def KakaoAuth(request):
    access_token = request.META.get('HTTP_AUTHORIZATION')

    user = get_userdata(access_token)

    # 토큰이 유효해서 사용자 정보를 가져오기 성공했으면
    if user:
        email = user.json().get('kakao_account').get('email')
        userdata = get_object_or_404(User, email = email)
        serializer = UserSerializer(userdata)
        user_id = serializer.data.get('id')
        profile_picture = serializer.data.get('profile_image')
        context = {
            'user_id' : user_id,
            "profile_picture" : profile_picture
        }
        return JsonResponse(context, status=status.HTTP_200_OK)
    
    # 토큰이 유효하지 않으면 로그인 페이지로 redirect
    else:
        login_url = 'http://127.0.0.1:8000/api/kakao'
        return redirect(login_url)

