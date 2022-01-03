from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login ,logout
from django.http import HttpResponse, JsonResponse, Http404
from .models import *


# Create your views here.
def login_user(request):
    msg=""
    if request.method=="POST":
        user=request.POST.get('username')
        password=request.POST.get('pass')
        u=authenticate(username=user,password=password)
        if u is not None:
            login(request,u)
            return render(request, "index.html",{'msg':"Login Successfull"})
            # pro
        else:
            msg="Either UserName Or Password Is Wrong"
            return render(request,"login.html",{'msg':msg})
    else:
        return render(request, "login.html")

def register(request):
    print("sucess"*100)
    if request.method=="POST":
        email= request.POST.get('email')
        username= request.POST.get('username')
        fname=request.POST.get('First_name')
        lname=request.POST.get('Last_name')
        print("dsfdsfd"*100)
        print(fname)
        User1= User.objects.all()
        msg=""
        print("success")
        val=False
        for u in User1:
            print(str(u.username))
            if str(u.username)==username:
                val=True
                break
        password=request.POST.get('password')
        if val:
            return render(request, "register.html",{'msg':"Username Already Exist!!"})
        
        
        else:
            user=User.objects.create(username=username,email=email,password=password,first_name=fname,last_name=lname)
            user.save()
            b= authenticate(user)
            if b is not None:
                return HttpResponse("PAge not Found")
                
            else:
                login(request,user)
                if request.POST.get("is_tutor")=="True":
                    return redirect('create_profile')
                else:
                    print(user.username)
                    return render(request, "profile.html",{'user':request.user})
    else:
        return render(request, "register.html")


