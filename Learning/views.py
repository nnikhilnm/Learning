from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def index(request):
    return render(request,"index.html")
