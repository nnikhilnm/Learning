from statistics import mode
from django.db import models
from datetime import datetime
from student.models import *

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, blank=True)


    
class Message(models.Model):
    value = models.CharField(max_length=1000000, blank=True)
    upload = models.FileField(upload_to ='static/media/', null=True, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=100000)
    room = models.CharField(max_length=100000)
    