from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['value', 'upload','user','room']