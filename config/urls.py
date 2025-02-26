from django.contrib import admin
from django.urls import path, include
from article.views import article_detail, article_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path('user/', include('apps.user.urls')),
    path("article/", include("apps.article.urls")),  # `article/urls.py` をルートにマッピング
    path("", article_list, name="home"),  # `http://localhost:8080/` で記事一覧を表示
    path("detail/<str:article_id>/", article_detail, name="article_detail"),
]
