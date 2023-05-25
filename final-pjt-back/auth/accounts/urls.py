from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('kakao', views.KakaoLogin, name='KakaoLogin'),
    path('kakao/callback', views.KakaoCallback, name='KakaoCallBack'),
    path('kakao/auth', views.KakaoAuth, name='KakaoAuth'),

    path('naver', views.NaverLogin, name='NaverLogin'),
    path('naver/callback', views.NaverCallback, name='NaverCallBack'),
    path('naver/auth', views.NaverAuth, name='NaverAuth'),
]
