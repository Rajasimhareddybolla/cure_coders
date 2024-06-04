from django.contrib.auth.models import User
from . import models
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login

# Create your views here.
def main(request):
    return HttpResponse('hello ')

def login_view(request):
    if request.method == "POST":
        name = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('User authenticated')
        else:
            return HttpResponse('Authentication failed')

    return render(request ,"blog/index.html")

def signup(request):
    if request.method == "POST":
        name = request.POST["username"]
        password = request.POST["password"]
        confirm = request.POST["c_password"]
        if password != confirm:
            print("fail")
            return render(request , "blog/signup.html" , {"message" : "error password and confirmation should be same"})
        n_user = models.MyUser.objects.create_user(username= name , password = password)
        n_user.save()
        print("sucess")
        return redirect('main')
    return render(request , "blog/signup.html")
def home(request):
    return render(request , "medicode/index.html")