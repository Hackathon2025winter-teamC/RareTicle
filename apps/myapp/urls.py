from django.contrib import
from django.urls import path
from .views import get_qiita_posts

urlpatterns = [
    path('artcles/', get_qiita_posts)
]