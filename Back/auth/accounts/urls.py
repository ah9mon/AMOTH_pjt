from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('kakao', views.KakaoLogin, name='KakaoLogin'),
    path('kakao/callback', views.KakaoCallback, name='KakaoCallBack'),
    path('kakao/auth', views.KakaoAuth, name='KakaoAuth'),
]
