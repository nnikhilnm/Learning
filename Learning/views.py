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
from datetime import timedelta
from student.forms import *
from chat.models import *
import os


def index(request):
    return render(request,"index.html")

def tutor(request):
    return render(request,"tutwel.html")

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
    bid = Bid.objects.all()
    list=[]
    count=0
    count1=0
    
    for b in bid:
        bd = b.tutor
        if bd.username == request.user and b.status=='Progress':
            count += 1
        if bd.username == request.user and b.status=='Completed':
            count1 += 1
    
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
        'user' : request.user,
        'count':count,
        'count1':count1,
    }
    return render(request, "tutor/projects.html", context)

def todo_list(request):
    bid = Bid.objects.all()
    li = []
    count=0
    count1=0
    count2=0
    for b in bid:
        bd = b.tutor
        print(b.project.date)
        
        print(b.day)
        print(int(b.day))
        b.project.date = b.project.date +timedelta(days=int(b.project.urgency))
        print(b.project.date)
        if bd.username == request.user:
            li.append(b)
        if bd.username == request.user and b.status=='Progress':
            count += 1
        if bd.username == request.user and b.status=='Delivered':
            count1 += 1
        if bd.username == request.user and b.status=='Completed':
            count2 += 1
    
    print(li)
    context = {
        'bid' : li,
        'count':count,
        'count1':count1,
        'count2':count2,
    }
    return render(request, "tutor/todo.html",context)


def Tutor_ticket(request):
    if request.method == "POST":
        ques_id = request.POST.get("question-id")
        description = request.POST.get("discription")
        print(ques_id)
        print(description)
        try:
            question = Question.objects.get(randomly_generated_id=ques_id)  
            ticket = TutorTicket.objects.create(question_id=str(ques_id),project=question,tutor=Tutor.objects.get(username=request.user),description=description)
            print(ticket)
            ticket.save()
        except:
            pass
        
    return render(request, "tutor/ticket.html")


####Login to kar
# password -1234

def stu_dashboard(request):
    user = User.objects.get(username = request.user)
    stu = Student.objects.get(username=user)
    question = Question.objects.filter(student=stu)
    # //////////////////
    bid = Bid.objects.all()
    count=0
    for b in bid:
        bd = b.project.student
        if bd.username == request.user and b.status=='Completed':
            count += 1
    # /////////////
    context = {
        'name': request.user,
        'question' : question,
        'count':count,
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
        que = Question.objects.filter(student=stu)
        qu = len(que)
        li = 0
        for q in que:
            bid = Bid.objects.filter(project=q)
            for b in bid:
                if b.status=='Completed':
                    li = li+1
        
        context = {
            'name': request.user,
            'errors':form.errors,
            'form':form,
            'stu':stu,
            'msg':msg,
            'que':qu,
            'aaa':li,
        }
        return render(request, "student/postquestion.html", context)
    else:
        form = QuestionForm()
        user = User.objects.get(username = request.user)
        stu = Student.objects.get(username=user)
        que = Question.objects.filter(student=stu)
        qu = len(que)
        li = 0
        for q in que:
            bid = Bid.objects.filter(project=q)
            for b in bid:
                if b.status=='Completed':
                    li = li+1

        context = {
            'name': request.user,
            'form':form,
            'stu':stu,
            'que':qu,
            'aaa':li,
        }
        return render(request, "student/postquestion.html", context)

def stu_ticket(request):
    if request.method == 'POST':
        ques_id = request.POST.get('ques_ID')
        mess = request.POST.get('message')
        try:
            question = Question.objects.get(randomly_generated_id=ques_id)  
            ticket = StudentTicket.objects.create(question_id=str(ques_id),project=question,student=Student.objects.get(username=request.user),description=mess)
            print(ticket)
            ticket.save()
        except:
            pass
    count=0
    bid = Bid.objects.all()
    count1=0
    for b in bid:
        bd = b.project.student
        if bd.username == request.user and b.status=='Completed':
            count1 += 1
        if bd.username == request.user:
            count += 1
    context = {
        'name': request.user,
        'que_completed': count1,
        'posted_que': count,
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
        tut = Tutor.objects.get(username=request.user)
        que = Question.objects.get(randomly_generated_id=desc)
        print(bid)
        print(tut)
        new_tutor = Bid.objects.create(tutor=tut,project=que,description=message,cost=bid,day="5")
        new_tutor.save()
        
        t = Tutor.objects.get(username=request.user)
        var = str(t.username.username) + "_" + str(que.student.username.username)
        print(var)
        
        room = Room.objects.all()
        flag=0
        for qu in room:
            if qu.name==var:
                flag=1
                break
        if flag==0:
            r=Room.objects.create(tutor=t,student=que.student,name=var)
            r.save()
            print(r)

        
        
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

        val = str(t.username.username) + " your bid for question(id->" + str(q.randomly_generated_id) + ") got selected"
        var = str(t.username.username) + "_" + str(q.student.username.username)
        t = Message.objects.create(value=val,user=request.user.username,room=var)
        t.save()        
        
        return redirect('stu_dashboard')
        
def message(request):
    user = User.objects.get(username = request.user)
    print(user)
    try:
        t=Tutor.objects.get(username=user)
        r=Room.objects.filter(tutor=t)
     
    except:
        s=Student.objects.get(username=user)
        r=Room.objects.filter(student=s)   

    return render(request, "message.html",{'room':r})

def todo_list_open(request):
    bid = Bid.objects.all()
    li = []
    count=0
    count1=0
    count2=0
    for b in bid:
        bd = b.tutor
        b.project.date = b.project.date +timedelta(days=int(b.project.urgency))
        if bd.username == request.user and b.status=='Open':
            li.append(b)
        if bd.username == request.user and b.status=='Progress':
            count += 1
        if bd.username == request.user and b.status=='Delivered':
            count1 += 1
        if bd.username == request.user and b.status=='Completed':
            count2 += 1
    context = {
        'bid' : li,
        'count':count,
        'count1':count1,
        'count2':count2,
    }
    return render(request, "tutor/todo.html",context)

def todo_list_progress(request):
    bid = Bid.objects.all()
    li = []
    count=0
    count1=0
    count2=0
    for b in bid:
        bd = b.tutor
        b.project.date = b.project.date +timedelta(days=int(b.project.urgency))
        if bd.username == request.user and b.status=='Progress':
            li.append(b)
            count += 1
        if bd.username == request.user and b.status=='Delivered':
            count1 += 1
        if bd.username == request.user and b.status=='Completed':
            count2 += 1
    
    print(li)
    context = {
        'bid' : li,
        'count':count,
        'count1':count1,
        'count2':count2,
    }
    return render(request, "tutor/todo.html",context)

def todo_list_declined(request):
    bid = Bid.objects.all()
    li = []
    count=0
    count1=0
    count2=0
    for b in bid:
        bd = b.tutor
        b.project.date = b.project.date +timedelta(days=int(b.project.urgency))
        if bd.username == request.user and b.status=='Declined':
            li.append(b)
        if bd.username == request.user and b.status=='Progress':
            count += 1
        if bd.username == request.user and b.status=='Delivered':
            count1 += 1
        if bd.username == request.user and b.status=='Completed':
            count2 += 1
    context = {
        'bid' : li,
        'count':count,
        'count1':count1,
        'count2':count2
    }
    return render(request, "tutor/todo.html",context)

def todo_list_delivered(request):
    bid = Bid.objects.all()
    li = []
    count=0
    count1=0
    count2=0
    for b in bid:
        bd = b.tutor
        b.project.date = b.project.date +timedelta(days=int(b.project.urgency))
        if bd.username == request.user and b.status=='Delivered':
            li.append(b)
            count1 += 1
        if bd.username == request.user and b.status=='Progress':
            count += 1
        if bd.username == request.user and b.status=='Completed':
            count2 += 1
    context = {
        'bid' : li,
        'count':count,
        'count1':count1,
        'count2':count2,
    }
    return render(request, "tutor/todo.html",context)


def todo_list_completed(request):
    bid = Bid.objects.all()
    li = []
    count=0
    count1=0
    count2=0
    for b in bid:
        bd = b.tutor
        b.project.date = b.project.date +timedelta(days=int(b.project.urgency))
        if bd.username == request.user and b.status=='Completed':
            li.append(b)
            count2 += 1
        if bd.username == request.user and b.status=='Progress':
            count += 1
        if bd.username == request.user and b.status=='Delivered':
            count1 += 1
    context = {
        'bid' : li,
        'count':count,
        'count1':count1,
        'count2':count2,
    }
    return render(request, "tutor/todo.html",context)

def todo_list_dispute(request):
    bid = Bid.objects.all()
    li = []
    count=0
    count1=0
    count2=0
    for b in bid:
        bd = b.tutor
        b.project.date = b.project.date +timedelta(days=int(b.project.urgency))
        if bd.username == request.user and b.status=='Dispute':
            li.append(b)
        if bd.username == request.user and b.status=='Progress':
            count += 1
        if bd.username == request.user and b.status=='Delivered':
            count1 += 1
        if bd.username == request.user and b.status=='Completed':
            count2 += 1
    context = {
        'bid' : li,
        'count':count,
        'count1':count1,
        'count2':count2,
    }
    return render(request, "tutor/todo.html",context)

def final_submit(request):
    pass