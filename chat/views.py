from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login ,logout
from django.http import HttpResponse, JsonResponse, Http404,HttpResponseRedirect
from .models import *
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from chat.models import Room, Message
from .forms import *

def home(request):
    user = User.objects.get(username = request.user)
    print(user)
    val=0
    try:
        s=Tutor.objects.get(username=user)
        r=Room.objects.filter(tutor=s)
    except:
        s=Student.objects.get(username=user)
        val=1
        r=Room.objects.filter(student=s)  

    
  
    return render(request, "message.html",{'room':r,'user':s,'val':val})

def room(request, room):
    user = request.user
    room_details = Room.objects.get(name=room)
    print(user)
    if request.user.is_authenticated:
        try:
            s=Tutor.objects.get(username=user)
            r=Room.objects.get(tutor=s)
        
        except:
            s=Student.objects.get(username=user)
            r=Room.objects.get(student=s) 
        
        print(s)

        if r.name==room:
            return render(request, 'chat/room.html', {
                'username': user.username,
                'room': room,
                'room_details': room_details
            })
        else:
            return render(request, 'login.html')
        
    else:
        return redirect('base')

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/chat/'+room+'/?username='+username)
    else:
        new_name = Room.objects.create(name=room)
        new_name.save()
        return redirect('/chat/'+room+'/?username='+username)


def send(request):
    print("sfdsfsdfsdfdfs")
    print( request.FILES)
    r=request.POST.get('room_info')
    form = MessageForm(request.POST, request.FILES)
    if form.is_valid():
        msg="Question Posted Successfully"
        form.save()
    else:
        print(form.errors)
    return HttpResponseRedirect("/chat/"+r)
        

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

def photoform(request):
    print('maa ak bhosada')
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        msg=""
        if form.is_valid():
            msg="Question Posted Successfully"
            form.save()
        else:
            print(form.errors)

    else:
        print('fail')
