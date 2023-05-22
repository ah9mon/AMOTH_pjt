from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404

# rest_framework
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# requests
import requests


# PAPAGO 언어 감지 
import os
import sys
import urllib.request
client_id_for_detect = settings.CLIENT_ID_FOR_DETECT
client_secret_for_detect = settings.CLIENT_SECRET_FOR_DETECT
client_id_for_translate = settings.CLIENT_ID_FOR_TRANSLATE
client_secret_for_translate = settings.CLIENT_SECRET_FOR_TRANSLATE
BASE_url = "https://openapi.naver.com/v1/papago/"


# Create your views here.

# 파파고api를 이용해 입력받은 q의 언어를 감지하는 함수
@api_view(['GET','POST'])
def detect_to_use_papago(request):
    q = request.GET.get('q')
    detect_url = f"{BASE_url}detectLangs"
    headers = {
        "X-Naver-Client-Id": client_id_for_detect,
        "X-Naver-Client-Secret": client_secret_for_detect
    }
    body = {
        "query" : q
    }
    detected = requests.post(detect_url,headers=headers,data=body)
    return Response(detected.json())

# 파파고 api를 이용해 text와 어느나라 언어인지를 입력하면 영어로 번역해주는 함수
@api_view(["GET","POST"])
def translate_to_use_papago(request):
    lang = request.GET.get('lang')
    q = request.GET.get('q')
    translate_url = f"{BASE_url}n2mt"
    headers = {
        "X-Naver-Client-Id" : client_id_for_translate,
        "X-Naver-Client-Secret" : client_secret_for_translate
    }
    body = {
        "source" : lang,
        "target" : "en",
        "text" : q
    }
    translated = requests.post(translate_url, headers=headers, data=body)
    # print(translated.json())
    return Response(translated.json())
