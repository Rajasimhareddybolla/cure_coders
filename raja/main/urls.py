from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("login/<str:name>" , views.login_view , name = "login"),
    path("signup" , views.signup , name = "signup"),
    path("home" , views.home , name = "home")
]