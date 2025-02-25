"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from article.views import article_detail, article_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path("articles/", include("article.urls")),  # `article/urls.py` をルートにマッピング
    path("", article_list, name="home"),  # `http://localhost:8080/` で記事一覧を表示
    path("detail/<str:article_id>/", article_detail, name="article_detail"),
]