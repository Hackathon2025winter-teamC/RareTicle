# from django.contrib import admin
from django.urls import path
from .views import register

urlpatterns = [
    path('signup/', register)
]