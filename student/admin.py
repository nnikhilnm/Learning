from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from .models import *

admin.site.register(Profile)
admin.site.register(Student)
admin.site.register(Tutor)