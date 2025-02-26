from django.urls import path
# from .views import IndexView, LoginView
from .views import article_list, article_detail

app_name = 'article'

urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    path("", article_list, name="article_list"),
    path("detail/<str:article_id>/", article_detail, name="article_detail"),
]
