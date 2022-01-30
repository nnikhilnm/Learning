from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from .models import *
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Question)
admin.site.register(Bid)
admin.site.register(TutorTicket)
admin.site.register(StudentTicket)