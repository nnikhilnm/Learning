from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.



class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=250, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    photo = models.FileField(null=True, blank=True)
    is_tutor= models.BooleanField(default=False)
    def __str__(self):
        return str(self.username) + str(' | ') + self.fullname
    
class Student(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
class Tutor(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    Education_status = models.CharField(max_length=250, null=True)
    Drive_link = models.URLField(max_length=300)
    Area_of_Expertise = models.CharField(max_length=250, null=True)