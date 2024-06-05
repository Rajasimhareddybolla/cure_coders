from openai import ChatCompletion
import openai
from datetime import timezone
from django.db import IntegrityError
import requests
from . import models
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login , logout 
from .models import MyUser

GROQ_API_KEY = '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'
GROQ_API_URL = 'https://api.groq.com/chat/completions'
# Create your views here.
def login_view(request):
    if request.method == "POST":
        is_hospital = request.POST.get('is_hospital', False)
        if not is_hospital:
            name = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=name, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            return redirect('signup')
        name = request.POST["username"]
        password = request.POST["password"]
        try:
            hospital = models.Hospital.objects.get(name=name, password=password)
            request.session['hospital_id'] = hospital.id
            
        except models.Hospital.DoesNotExist:
            return redirect("home")
        return redirect("hospitals")  # Corrected here

    return render(request ,"blog/index.html")

def hospitals(request):
    hospital_id = request.session.get('hospital_id')
    print(str(hospital_id) +'kddk')
    if hospital_id is not None:
        hospital = models.Hospital.objects.get(id=hospital_id)
        specialists = hospital.specialists.all()
        num_beds = hospital.num_beds
        schedule = hospital.schedule
        total_patients = hospital.total_patients
        total_doctors = hospital.total_doctors
        dis = hospital.description
        print(specialists)
        past_appointments = hospital.appointments.all()
        print(past_appointments)
        # Prepare the data to send to the template
        data = {
            "url" : dis,
            "past_appointments":past_appointments,
            'specialists' : specialists,
            'hospital': hospital.name,
            'num_beds': num_beds,
            'schedule': schedule,
            'total_patients': total_patients,
            'total_doctors': total_doctors,
        }
        return render(request, "hospitals/index.html", data)  # Corrected here
    print("foold")
    return render(request, "hospitals/index.html")  # Corrected here
# class Hospital(models.Model):
#     name = models.CharField(max_length=255)
#     url = models.TextField()
#     location = models.TextField()
#     specialists = models.ManyToManyField(Specialist)
#     stats = models.TextField()
#     description = models.TextField()
#     password = models.CharField(max_length= 64 , default="raja")
#     num_beds = models.PositiveIntegerField(default=0)
#     schedule = models.TextField(default= "22")
#     total_patients = models.PositiveIntegerField(default=0)
#     total_doctors = models.PositiveIntegerField(default=0)
from django.contrib import messages

def signup(request):
    if request.method == "POST":
        is_hospital = request.POST.get('is_hospital', 'False') == 'True'
        name = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("c_password")
        url = request.POST.get("url")

        if not all([name, password, confirm, url]):
            messages.error(request, "All fields must be filled out.")
            return render(request , "blog/index.html")

        if password != confirm:
            messages.error(request, "Password and confirmation should be the same.")
            return render(request , "blog/index.html")

        try:
            if not is_hospital:
                n_user = models.MyUser.objects.create_user(username=name, password=password, image=url)
            else:
                n_user = models.Hospital(name=name, password=password, url=url)
            n_user.save()
        except Exception as e:
            messages.error(request, str(e))
            return render(request , "blog/index.html")

        messages.success(request, "Success")
        return redirect('main')

    return render(request , "blog/index.html")
def home(request):
    if request.user.is_authenticated:
        hosipetal = models.Hospital.objects.all().values()
        return render(request , "medicode/index.html" , {"hospitels":hosipetal})
    return redirect('signup')

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        url = request.POST["url"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "main/register.html", {   #pending direct to the register page 
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = MyUser(username = username,email= email,password= password,image = url)
            user.save()
        except IntegrityError:
            return render(request, "main/register.html", {
                "message": "Username already taken."
            })
        login( request,user)
        return redirect("home")
    else:
        return render(request, "main/login.html")

def Logout(request):
    logout(request)
    return redirect('signup')
def about(request):
    return render(request, 'medicode/about.html')

def doctors(request):
    return render(request, 'medicode/doctor.html')

def department(request):
    return render(request, 'medicode/department.html')


def elements(request):
    return render(request, 'medicode/elements.html')

def contact(request):
    #     user = models.CharField(max_length=255)
    # message = models.TextField()
    # email = models.EmailField()
    # subject = models.CharField(max_length=444)
    # resolved = models.BooleanField(default=False)
    if request.method == "POST":
        user = MyUser.objects.get(id=request.user.id)
        email = request.POST["email"]
        message = request.POST['message']
        name = request.POST['name']
        subject = request.POST['subject']
        comm = models.comments(user = user , message = message , email = email , subject = subject)
        comm.save()
        return HttpResponse("sucess")
    return render(request, 'medicode/contact.html')
def appointment(request):
    #     user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="appointments")
    # hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="appointments")
    # datetime = models.DateTimeField()
    # comments = models.TextField()
    if request.method == "POST":
        
        user = MyUser.objects.get(id=request.user.id)
        hospitel = models.Hospital.objects.get(id =  request.POST["hospitel"])
        datetime = request.POST["datetime"]
        comments = request.POST["comments"]
        appo = models.Appointment(user = user , hospital = hospitel ,datetime =  datetime , comments = comments)
        appo.save()
        return HttpResponse("sucess"+str(appo))
    return redirect("home")
    
def hospitels(request):
    return render(request , 'hospitels/index.html')
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def bot_r(request):
    conversation = request.session.get('conversation', [])
    if request.method == "POST":
        message = request.POST.get('message', '')
        prompts = []
        conversation.append({"role": "user", "content": message})
        prompts.extend(conversation)
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompts,
            api_key="" # apply your api key hear
        )
    
        chatbot_replies = [message['message']['content'] for message in response['choices'] if message['message']['role'] == 'assistant']

        # Append chatbot replies to the conversation
        for reply in chatbot_replies:
            conversation.append({"role": "assistant", "content": reply})
        print(conversation)
        request.session['conversation'] = conversation
        return render(request, 'chat.html', {'user_input': message, 'chatbot_replies': chatbot_replies, 'conversation': conversation})
    else:
        request.session.clear()
        return render(request, 'chat.html', {'conversation': conversation})
def form(request):
    return render(request , "blog/ts.html")
def profile(request):
    user_image = None
    if request.user.is_authenticated and request.user:
        user_image = models.MyUser.objects.get(id = request.user.id)
        user_image = user_image.image
    return render(request, 'blog/profile.html', {'image': user_image})