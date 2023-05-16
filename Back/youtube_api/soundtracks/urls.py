from django.urls import path
from . import views

app_name = 'soundtracks'
urlpatterns = [
    path('soundtrack', views.get_soundtrack, name="soundtrack"),
]