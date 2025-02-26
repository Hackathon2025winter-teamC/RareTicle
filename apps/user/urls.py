# from django.contrib import admin
from django.urls import path
from .views import signup, login_view, logout_view
from django.contrib.auth.views import LogoutView

app_name = "user"

urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout")
]