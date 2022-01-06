from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login ,logout
from django.http import HttpResponse, JsonResponse, Http404
from .models import *
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings


# Create your views here.
def login_user(request):
    msg=""
    if request.method=="POST":
        user=request.POST.get('username')
        password=request.POST.get('pass')
        print(user + "  " + password)
        print(User.objects.get(username="kapilagrawal").password)
        u=authenticate(username=user,password=password)
        print(u)
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
    if request.method=="POST":
        email= request.POST.get('email')
        username= request.POST.get('username')
        fname=request.POST.get('First_name')
        lname=request.POST.get('Last_name')

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
                    tutor = Tutor.objects.create(username=user)
                    return redirect('create_profile')
                else:
                    student = Student.objects.create(username=user)
                    student.save()
                    print(user.username)
                    return render(request, "profile.html",{'user':request.user})
    else:
        return render(request, "register.html")

def Forgot(request):
    if request.method=='POST':
        Email = request.POST.get('Email')
        user = User.objects.get(email=Email) 
        
        if not user:
            messages.success(request, 'User not found') 
            return redirect(request, "Password.html")
        else:
            email = EmailMessage(
                'Reset your password', 'Kapil this is your reset link', settings.EMAIL_HOST_USER, to=[Email]
            )
            email.send(fail_silently=True)
            return render(request, "reset_password.html")
    else:
        return render(request, "Password.html")
  
