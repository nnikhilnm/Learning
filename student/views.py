from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Create your views here.
def login(request):
    if request.method=="POST":
        email= request.POST.get('email')
        username= request.POST.get('username')
        password=request.POST.get('password')
        user=User.objects.create(username=username,email=email,password=password)
        user.save()
        return render(request, "login.html")
    else:
        return render(request, "login.html")