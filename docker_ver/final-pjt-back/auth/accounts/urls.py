from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("kakao", views.process_kakao_login, name="KakaoLogin"),
    path("kakao/callback", views.process_kakao_callback, name="KakaoCallBack"),
    path("kakao/auth", views.process_kakao_auth, name="KakaoAuth"),

    path("naver", views.process_naver_login, name="NaverLogin"),
    path("naver/callback", views.process_naver_callback, name="NaverCallBack"),
    path("naver/auth", views.process_naver_auth, name="NaverAuth"),
]

