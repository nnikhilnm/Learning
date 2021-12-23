from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse, Http404
from .models import *


# Create your views here.
def login(request):
    if request.method=="POST":
        email= request.POST.get('email')
        username= request.POST.get('username')
        User1= User.objects.all()
        msg=""
        val=False
        for u in User1:
            print(str(u.username))
            if str(u.username)==username:
                val=True
                break
        password=request.POST.get('password')
        if val:
            return render(request, "login.html",{'msg':"Username Already Exist!!"})
        
        
        else:
            user=User.objects.create(username=username,email=email,password=password)
            user.save()
            b= authenticate(user)
            if b is not None:
                login(request,user)
                return HttpResponse("PAge not Found")
                
            else:
                return render(request, "profile.html",{'user':request.user})
    else:
        return render(request, "login.html")