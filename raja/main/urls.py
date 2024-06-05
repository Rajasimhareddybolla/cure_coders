from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="main"),
    path("login" , views.login_view , name = "login"),
    path("signup" , views.signup , name = "signup"),
    path("home" , views.home , name = "home"),
    path("register" , views.register , name="register"),
    path("Logout" , views.Logout , name= "Logout"),
    path('about/', views.about, name='about'),
    path('doctors/', views.doctors, name='doctors'),
    path('department/', views.department, name='department'),

    path('elements/', views.elements, name='elements'),
    path('contact/', views.contact, name='contact'),
    path("Appointment" , views.appointment , name="Appointment"),
    path("hospitals" , views.hospitals , name= "hospitals"),
    path("bot" , views.bot_r , name = "bot"),
    path("profile", views.profile, name="profile"),
    path("form" , views.form , name= "form")
    ]