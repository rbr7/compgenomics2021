from django.urls import path
from hello_webserver import views

urlpatterns = [
    path("", views.home, name="home"),
]