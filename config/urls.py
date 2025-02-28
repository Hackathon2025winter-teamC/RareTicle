from django.contrib import admin
from django.urls import path, include
from apps.article.views import article_detail, article_list
from apps.user.views import login_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", login_view),
    path('user/', include('apps.user.urls')),
    path("article/", include("apps.article.urls")),  # `article/urls.py` をルートにマッピング
]
