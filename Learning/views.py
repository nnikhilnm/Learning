from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login ,logout
from django.http import HttpResponse, JsonResponse, Http404
from student.models import *
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings

def index(request):
    return render(request,"index.html")

def create_profile(request):
    return render(request, "tutor/create_profile.html",{'user':request.user})

def dashboard(request):
    user=Tutor.objects.get(username=request.user)
    question=Bid.objects.filter(tutor=user)
    print(question)
    for q in question:
        print(q.project)
    context={
        'user' : request.user,
        'question' :question
    }
    return render(request, "tutor/dashboard.html", context)