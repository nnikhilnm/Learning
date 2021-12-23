from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.



class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=250, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    photo = models.FileField(null=True, blank=True)
    def __str__(self):
        return str(self.username) + str(' | ') + self.fullname