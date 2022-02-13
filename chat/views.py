from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login ,logout
from django.http import HttpResponse, JsonResponse, Http404
from .models import *
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from chat.models import Room, Message
def home(request):
    user = User.objects.get(username = request.user)
    print(user)
    try:
        t=Tutor.objects.get(username=user)
        r=Room.objects.filter(tutor=t)
     
    except:
        s=Student.objects.get(username=user)
        r=Room.objects.filter(student=s)   

    return render(request, "message.html",{'room':r})

def room(request, room):
    username = request.user.username
    room_details = Room.objects.get(name=room)
    return render(request, 'chat/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

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
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})