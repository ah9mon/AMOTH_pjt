from django.urls import path
from . import views

urlpatterns = [
    path("papago/detect", views.detect_to_use_papago, name="papago_detect"),
    path("papago/translate", views.translate_to_use_papago, name="papago_translate"),
]