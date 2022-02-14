from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login ,logout
from django.http import HttpResponse, JsonResponse, Http404
from .models import *
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
import math
import random

# Create your views here.
def login_user(request):
    msg=""
    if request.method=="POST":
        user=request.POST.get('username')
        password=request.POST.get('pass')
        print(user + "  " + password)
        u=authenticate(username=str(user),password=str(password))
        print(u)
        if u is not None:
            
            login(request,u)
            User1=User.objects.get(username=user)
            print(User1)
            print("success1")
            try :
                t=Tutor.objects.get(username=User1)
                print("SDfsdfgsdfdsg")
                return redirect('dashboard')
                
            except :
                s=Student.objects.get(username=User1)
                return redirect("stu_dashboard")
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
        val=1
        for u in User1:
            print(str(u.username))
            if str(u.username)==username:
                val=2
            elif str(u.email)==email:
                val=3
            if val==2 or val==3:
                break
            
        password=request.POST.get('password')
        if val==2:
            return render(request, "register.html",{'msg':"Username Already Exist!!"})
        elif val==3:
            return render(request, "register.html",{'msg':"Email Already Exist!!"})
        
        
        else:
            user=User.objects.create_user(username=username,email=email,password=password,first_name=fname,last_name=lname)
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
                    return redirect('student:createprofile')
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
            OTP = ""
            string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            length = len(string)
            for i in range(6) :
                OTP += string[math.floor(random.random() * length)]
            subject = f'Your UserName is {user.username} One Time Password (OTP) for password reset: '
            email2 = EmailMessage(
                        subject, OTP, settings.EMAIL_HOST_USER, to=[Email]
                            )
            print(email2)
            email2.send(fail_silently=True)
            print(OTP)
            request.session['OTP'] = OTP
            
            context = {
                'email':Email,
            }
            return render(request, "reset_password.html", context)
    else:
        return render(request, "Password.html")
    
def reset_passward(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        print(user)
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')
  
def createprofile(request):
    if request.method=="POST":
        try:
            student = Student.objects.get(username=request.user)
            student.gender=request.POST.get('gender')
            student.fullname=User.objects.get(username=request.user).first_name+" "+User.objects.get(username=request.user).last_name
            student.avtar="https://avatars.dicebear.com/api/"+str(request.POST.get('gender'))+'/'+User.objects.get(username=request.user).first_name+".svg"
            student.save()
            return redirect('stu_dashboard')
        except:
            return redirect('student:login')
    else:        
        return render(request,'student/createprofile.html')
    
def Forgot_reset(request):
    if request.method == 'POST':
        otp=request.POST.get('otp')
        new_pass1 = request.POST.get('pass1')
        new_pass2 = request.POST.get('pass2')
        email = request.POST.get('email')
        u = User.objects.get(email=email)
        if new_pass1 == new_pass2 and otp== request.session['OTP']:
            u.set_password(new_pass2)
            print(u.password)
            u.save()
            print(u)
            return redirect('student:login')
        else:
            msg="Otp / Password Incorrect "
            context={
                'msg':msg,
                'email':email
            }
            return render(request,"reset_password.html", context)
    else:
        return render(request,'student/createprofile.html')