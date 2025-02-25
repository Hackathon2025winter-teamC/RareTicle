from django.urls import path
from .views import article_list, article_detail

urlpatterns = [
    path("", article_list, name="article_list"),
    path("detail/<str:article_id>/", article_detail, name="article_detail"),
]
