# 新規
from django.urls import path, include
from . import views

app_name = "diary"
url_patterns = [
    path("", views.index, name="index"),
    path('', include('health_check.urls'))
]
