import re
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login ,logout
from django.http import HttpResponse, JsonResponse, Http404
from student.models import *
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
import datetime 
from student.forms import *
import os


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
    user=Tutor.objects.get(username=request.user)
    bid_question=Bid.objects.filter(tutor=user)
    list=[]
    for q in question:
        flag=0
        for b in bid_question:
            if b.project==q:
                flag=1
                break
        if flag==0:
            list.append(q)
    print(list)

    print("<<<<----This is projects part---->>>>")
    print(question)
    for q in question:
        print(q.student)
    context = {
        'question' : list,
        'user' : request.user
    }
    return render(request, "tutor/projects.html", context)

def todo_list(request):
    bid = Bid.objects.all()
    li = []
    for b in bid:
        bd = b.tutor
        print(b.project.date)
        
        print(b.day)
        print(int(b.day))
        b.project.date = b.project.date + datetime.timedelta(days=int(b.project.urgency))
        print(b.project.date)
        if bd.username == request.user:
            li.append(b)
    
    print(li)
    context = {
        'bid' : li
    }
    return render(request, "tutor/todo.html",context)


def ticket(request):
    if request.method == "POST":
        ques_id = request.POST.get("question-id")
        description = request.POST.get("discription")
        print(ques_id)
        print(description)
        ticket = Ticket.objects.create(question_id=str(ques_id),tutor=Tutor.objects.get(username=request.user),description=description)
        print(ticket)
        ticket.save()
    return render(request, "tutor/ticket.html")

####Login to kar
# password -1234

def stu_dashboard(request):
    user = User.objects.get(username = request.user)
    stu = Student.objects.get(username=user)
    question = Question.objects.filter(student=stu)
    context = {
        'name': request.user,
        'question' : question,
    }
    return render(request, "student/index.html", context)

def Post_question(request):
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        msg=""
        # print(form)
        if form.is_valid():
            # file is saved
            msg="Question Posted Successfully"
            form.save()
        else:
            print(form.errors)
        
        # cat = request.POST.get('radio')
        # print(cat)
        
        # date = datetime.date.today()
        # print(date)
        # current_time = datetime.datetime.now()
        # time = current_time.strftime("%H:%M:%S")
        # print(time)
        
        # description = request.POST.get('description')
        # urgency = request.POST.get('urgency')
        # # zip = ModelWithFileField(file_field=request.FILES['myFile'])
        # # handle_uploaded_file(request.FILES['myFile'])
        # # print(zip)
        # user = User.objects.get(username = request.user)
        # stu = Student.objects.get(username=user)
        
        # que = Question.objects.create(student=stu,category=cat,urgency=urgency,description=description,date=date,time=time)
        # k=que(upload=request.FILES['myFile'])
        # k.save()
        # que.save()
        form = QuestionForm()
        user = User.objects.get(username = request.user)
        stu = Student.objects.get(username=user)
        
        context = {
            'name': request.user,
            'errors':form.errors,
            'form':form,
            'stu':stu,
            'msg':msg
        }
        return render(request, "student/postquestion.html", context)
    else:
        form = QuestionForm()
        user = User.objects.get(username = request.user)
        stu = Student.objects.get(username=user)
        context = {
            'name': request.user,
            'form':form,
            'stu':stu
        }
        return render(request, "student/postquestion.html", context)

def stu_ticket(request):
    context = {
        'name': request.user
    }
    return render(request, 'student/ticket.html', context)

def stu_bid(request, myid):
    que = Question.objects.get(id=myid)
    print(myid)
    bid = Bid.objects.filter(project=que)
    print(bid)
    context = {
        'name': request.user,
        'bid' : bid
    }
    return render(request, 'student/bid.html', context)

def create_bid(request):
    if request.method == 'POST':
        bid = request.POST.get('Bid')
        message = request.POST.get('message')
        desc = request.POST.get('urls')
        print(f"<<<<<<<<------skdnboubw/////--{desc}---->><<djcbiwbi--------->>>>>>>>>")
        tut = Tutor.objects.get(username=request.user)
        que = Question.objects.get(randomly_generated_id=desc)
        print(bid)
        print(tut)
        new_tutor = Bid.objects.create(tutor=tut,project=que,description=message,cost=bid,day="5")
        new_tutor.save()
        return redirect("projects")
    else:
        return render(request, 'student/bid.html')

def logout_user(request):
    logout(request)
    return redirect('base')

def bid_approve(request):
    if request.method=='POST':
        t=Tutor.objects.get(id=request.POST.get('tutor_id'))
        q=Question.objects.get(id=request.POST.get('ques_id'))
        b=Bid.objects.get(tutor=t,project=q)
        b.status='Progress'
        b.save()
        all_bid=Bid.objects.filter(project=q)
        for bid in all_bid:
            if bid!=b:
                bid.status='Declined'
                bid.save()
        
        print(t)
        print(b)
        return redirect('stu_dashboard')
        