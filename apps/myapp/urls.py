from django.contrib import admin, include
from django.urls import path

url_patterns = [
    path('', include('health_check.urls'))
]