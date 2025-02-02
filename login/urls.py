from django.urls import path
from apps.myapp.views import login  # Import the index view

urlpatterns = [
    path("", login, name="login"),  # Map the root URL to the index view
]