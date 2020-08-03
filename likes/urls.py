from django.urls import path
from . import views

# start with blog
urlpatterns = [
    # http://localhost:8000/blog/1
    path('like_change', views.like_change, name="like_change"),
]