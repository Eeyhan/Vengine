from django.urls import path, re_path, include
from app1 import views

urlpatterns = [
    path('video', views.VideoView.as_view())
]
