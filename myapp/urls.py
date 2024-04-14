from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("teammembers/", views.team_members, name="teammembers"),
    path("chat/", views.chat, name="chat"),
    path("getResponse", views.getResponse, name='getResponse'),
]