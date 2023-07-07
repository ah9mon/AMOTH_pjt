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

KAKAO_KEY = settings.KAKAO_KEY
KAKAO_USER_URL = "https://kapi.kakao.com"
KAKAO_AUTH_URL = "https://kauth.kakao.com"

NAVER_CLIENT_ID = settings.NAVER_CLIENT_ID
NAVER_CLIENT_SECRET = settings.NAVER_CLIENT_SECRET
NAVER_BASE_URL = "https://nid.naver.com/oauth2.0/"

# Create your views here.

def get_userdata(access_token):
    '''
    Get user data using the access_token.

    Parameters:
    - access_token: Access token used to request user information.

    Returns:
    - User data obtained from the API.
    '''
    headers = {'Authorization': f'Bearer {access_token}'}
    user_url = f'{KAKAO_USER_URL}/v2/user/me'
    user = requests.get(user_url, headers=headers)
    return user

def get_access_token(code):
    '''
    Get access_token using the authorization code.

    Parameters:
    - code: Authorization code used to request the access_token.

    Returns:
    - Access token obtained from the API.
    '''
    data = {
        'client_id': KAKAO_KEY,
        'grant_type': 'authorization_code',
        'redirection_uri': 'http://127.0.0.1:8000/api/kakao',
        'code': code
    }
    token_url = f'{KAKAO_AUTH_URL}/oauth/token'
    token_data = requests.post(token_url, data=data).json()
    access_token = token_data.get('access_token')
    return access_token

def process_kakao_login(request):
    '''
    Process Kakao login.

    Redirects to Kakao authorization URL to initiate the login process.
    '''
    redirect_uri = 'http://127.0.0.1:8000/api/kakao/callback'
    url = f'{KAKAO_AUTH_URL}/oauth/authorize?client_id={KAKAO_KEY}&redirect_uri={redirect_uri}&response_type=code'
    return redirect(url)

def process_kakao_callback(request):
    '''
    Process the callback after Kakao login authorization.

    Retrieves the access_token using the authorization code and fetches user data.
    If the user does not exist, saves the user information in the database.
    Redirects to the login page with the access_token and source as query parameters.
    '''
    code = request.GET.get('code')
    access_token = get_access_token(code)
    user = get_userdata(access_token).json()
    nickname = user.get('properties').get('nickname')
    profile_image = user.get('properties').get('profile_image')
    email = user.get('kakao_account').get('email')
    userdata = {
        'nickname': nickname,
        'profile_image': profile_image,
        'email': email
    }
    serializer = UserSerializer(data=userdata)
    users = User.objects.all()
    if serializer.is_valid(raise_exception=True):
        existing_user = users.filter(email=email)
        if not existing_user:
            serializer.save()
    redirect_url = f'http://localhost:8080/login?access_token={access_token}&source=kakao'
    return HttpResponseRedirect(redirect_url)

def process_kakao_auth(request):
    '''
    Process Kakao authentication.

    Retrieves the access_token from the request headers.
    If the token is valid, fetches user data and returns it as a JSON response.
    Otherwise, redirects to the login page.
    '''
    access_token = request.META.get('HTTP_AUTHORIZATION')
    user = get_userdata(access_token)
    if user:
        email = user.json().get('kakao_account').get('email')
        userdata = get_object_or_404(User, email=email)
        serializer = UserSerializer(userdata)
        user_id = serializer.data.get('id')
        profile_picture = serializer.data.get('profile_image')
        context = {
            'user_id': user_id,
            'profile_picture': profile_picture
        }
        return JsonResponse(context, status=status.HTTP_200_OK)
    else:
        login_url = 'http://127.0.0.1:8080/login'
        return redirect(login_url)

def process_naver_login(request):
    '''
    Process Naver login.

    Redirects to Naver authorization URL to initiate the login process.
    '''
    redirect_uri = 'http://127.0.0.1:8000/api/naver/callback'
    url = f'{NAVER_BASE_URL}authorize?response_type=code&client_id={NAVER_CLIENT_ID}&redirect_uri={redirect_uri}&state=test'
    return redirect(url)

def process_naver_callback(request):
    '''
    Process the callback after Naver login authorization.

    Retrieves the access_token using the authorization code and fetches user data.
    If the user does not exist, saves the user information in the database.
    Redirects to the login page with the access_token and source as query parameters.
    '''
    code = request.GET.get('code')
    state = request.GET.get('state')
    url = f'{NAVER_BASE_URL}token?grant_type=authorization_code&client_id={NAVER_CLIENT_ID}&client_secret={NAVER_CLIENT_SECRET}&redirect_uri=http://127.0.0.1:8000/api/naver/callback&code={code}&state={state}'
    headers = {
        'X-Naver-Client-Id': NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': NAVER_CLIENT_SECRET
    }
    res = requests.get(url, headers=headers).json()
    access_token = res.get('access_token')
    url = 'https://openapi.naver.com/v1/nid/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    user = requests.get(url, headers=headers).json()
    nickname = user.get('response').get('name')
    profile_image = user.get('response').get('profile_image')
    email = user.get('response').get('email')
    userdata = {
        'nickname': nickname,
        'profile_image': profile_image,
        'email': email
    }
    serializer = UserSerializer(data=userdata)
    users = User.objects.all()
    if serializer.is_valid(raise_exception=True):
        existing_user = users.filter(email=email)
        if not existing_user:
            serializer.save()
    redirect_url = f'http://localhost:8080/login?access_token={access_token}&source=naver'
    return HttpResponseRedirect(redirect_url)

def process_naver_auth(request):
    '''
    Process Naver authentication.

    Retrieves the access_token from the request headers.
    If the token is valid, fetches user data and returns it as a JSON response.
    Otherwise, redirects to the login page.
    '''
    access_token = request.META.get('HTTP_AUTHORIZATION')
    url = 'https://openapi.naver.com/v1/nid/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    user = requests.get(url, headers=headers).json()
    if user:
        email = user.get('response').get('email')
        userdata = get_object_or_404(User, email=email)
        serializer = UserSerializer(userdata)
        user_id = serializer.data.get('id')
        profile_picture = serializer.data.get('profile_image')
        context = {
            'user_id': user_id,
            'profile_picture': profile_picture
        }
        return JsonResponse(context, status=status.HTTP_200_OK)
    else:
        login_url = 'http://localhost:8080/login'
        return redirect(login_url)
