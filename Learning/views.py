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
    if request.method == "POST":
        edu = request.POST.get("education")
        link = request.POST.get("proof")
        area = request.POST.get("area")
        tutor = Tutor.objects.get(username=request.user)
        tutor.Education_status=edu
        tutor.Drive_link=link
        tutor.Area_of_Expertise=area
        tutor.save()
        return redirect('dashboard')
    else:
        return render(request, "tutor/create_profile.html",{'user':request.user})

def dashboard(request):
    user=Tutor.objects.get(username=request.user)
    question=Bid.objects.filter(tutor=user)
    print(question)
    rating=0
    count=0
    for q in question:
        print(q.project)
        if q.is_selected :
            count+=1
            print(q.rating)
            rating=q.rating
    if count:
        rating=rating/count
    print(rating)
    context={
        'user' : request.user,
        'question' :question,
        'rating' :rating
    }
    return render(request, "tutor/dashboard.html", context)

def projects(request):
    question = Question.objects.all()
    print("<<<<----This is projects part---->>>>")
    print(question)
    for q in question:
        print(q.student)
    context = {
        'question' : question,
    }
    return render(request, "tutor/projects.html", context)

def todo_list(request):
    return render(request, "tutor/todo.html")

def ticket(request):
    return render(request, "tutor/ticket.html")