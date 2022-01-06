from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.

class Tutor(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    Qualification = models.CharField(blank=True)
    Certificate = models.FileField(null=True, blank=True)